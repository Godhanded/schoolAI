from flask import jsonify, request, Blueprint
import openai
import os
from schoolAI.schemas import TopicSchema
from pydantic import ValidationError
from schoolAI.errors.handlers import CustomError
from schoolAI.models import ExplainedTopics, Users
from schoolAI.auth.auth import requires_auth
from schoolAI.utils import explain, raise_input_error

interaction = Blueprint("interaction", __name__)

openai.api_key = os.getenv("OPENAI_KEY")


@interaction.route("/explain", methods=["POST"])
@requires_auth(request=request)
def explain_topic(payload):
    id = payload.get("user_id")
    data = request.get_json()
    try:
        data = TopicSchema(**data)
    except ValidationError as e:
        raise_input_error(e)

    explanations = {}
    for topic in data.topics:
        explanation = explain(topic)
        explanations[topic] = explanation
        explained_topic = ExplainedTopics.query.filter_by(topic=topic).first()
        if explained_topic:
            explained_topic.explanation = explanation
            explained_topic.update()
        else:
            data = ExplainedTopics(user_id=id, topic=topic, explanation=explanation)
            data.insert()
    return (
        jsonify(
            {
                "status": True,
                "message": "sucessfully explianed",
                "explained_topics": explanations,
            }
        ),
        200,
    )


@interaction.route("/history")
@requires_auth(request)
def get_explanation_history(payload):
    id = payload.get("user_id")

    user = Users.query.get(id)
    if not user:
        raise CustomError("Unauthorized", 401, "User does not exist")
    user_topics = [data.format() for data in user.topics]
    return jsonify({"status": True, "history": user_topics, "message": "success"}), 200

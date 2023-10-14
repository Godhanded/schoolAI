from flask import jsonify, request, Blueprint
import openai
import os
from schoolAI.errors.handlers import UtilError
from schoolAI.models import ExplainedTopics, Users
from schoolAI.auth.auth import requires_auth
from schoolAI.utils import explain

interaction = Blueprint("interaction", __name__)

openai.api_key = os.getenv("OPENAI_KEY")


@interaction.route("/explain", methods=["POST"])
@requires_auth(request=request)
def explain_topic(payload):
    id = payload.get("user_id")
    data = request.get_json()
    topics = data.get("topics")
    if not topics:
        raise UtilError("Bad Request", 400, "Please provide valid topic")

    explanations = {}
    for topic in topics:
        explanation = explain(topic)
        explanations[topic] = explanation
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
        raise UtilError("Unauthorized", 401, "User does not exist")
    user_topics = [data.format() for data in user.topics]
    return jsonify({"status": True, "history": user_topics, "message": "success"}), 200

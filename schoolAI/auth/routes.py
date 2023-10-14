from flask import jsonify, request, Blueprint
from schoolAI.models import Users
from schoolAI.errors.handlers import UtilError
from schoolAI.auth.auth import requires_auth, encode_jwt
from schoolAI import bcrypt


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def signup():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    if not email or not password:
        raise UtilError("Bad Request", 400, "Missing required fields")

    user = Users.query.filter_by(email=email).one_or_none()
    if user:
        raise UtilError("Forbidden", 403, "This user alread exists")

    user = Users(
        email=email, password=bcrypt.generate_password_hash(password).decode("utf-8")
    )
    user.insert()

    return (
        jsonify(
            {
                "status": True,
                "message": "success",
                "token": encode_jwt(user.id),
                "user": user.format(),
            }
        ),
        201,
    )


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    if not email or not password:
        raise UtilError("Bad Request", 400, "Missing Required fields")
    user = Users.query.filter_by(email=email).one_or_none()
    if not user:
        raise UtilError("Unauthorized", 401, "User does not exist")
    if not bcrypt.check_password_hash(user.password, password):
        raise UtilError("Unauthorized", 401, "Passwords do not match")
    return (
        jsonify(
            {
                "status": True,
                "message": "success",
                "user": user.format(),
                "token": encode_jwt(user.id)
            }
        ),
        200,
    )


@auth.route("/@me")
@requires_auth(request=request)
def get_loged_in_user(payload):
    id = payload.get("user_id")
    user = Users.query.get(id)
    if not user:
        raise UtilError("Unauthorized", 401, "Invalid token")
    return jsonify({"status": True, "message": "success", "user": user.format()}), 200

from flask import Blueprint, jsonify
from schoolAI.auth.auth import AuthError
from schoolAI import db

error = Blueprint("error", __name__)


class UtilError(Exception):
    def __init__(self, error, code, message):
        self.error = error
        self.code = code
        self.message = message


@error.teardown_app_request
def clean_up(exc):
    try:
        db.session.remove()
    except:
        pass


@error.app_errorhandler(UtilError)
def resource_not_found(err):
    return (
        jsonify({"error": err.error, "status": True, "message": err.message}),
        err.code,
    )


@error.app_errorhandler(AuthError)
def auth_error(err):
    return (
        jsonify(
            {"error": "Authorization Error", "status": True, "message": err.message}
        ),
        err.status_code,
    )


@error.app_errorhandler(400)
def bad_request(error):
    return (
        jsonify({"error": error.name, "status": True, "message": error.description}),
        400,
    )


@error.app_errorhandler(404)
def resource_not_found(error):
    return (
        jsonify({"error": error.name, "status": True, "message": error.description}),
        404,
    )


@error.app_errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"error": error.name, "status": True, "message": error.description}),
        405,
    )


@error.app_errorhandler(422)
def cant_process(error):
    return (
        jsonify({"error": error.name, "status": True, "message": error.description}),
        422,
    )


@error.app_errorhandler(429)
def cant_process(error):
    return (
        jsonify({"error": error.name, "status": True, "message": error.description}),
        429,
    )


@error.app_errorhandler(500)
def server_error(error):
    return (
        jsonify({"error": error.name, "status": True, "message": "Its not you its us"}),
        500,
    )

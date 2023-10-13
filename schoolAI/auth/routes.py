from flask import jsonify, request, Blueprint
from schoolAI.models import User
from schoolAI import bcrypt
from schoolAI.utils import (
    query_one_filtered,
)



auth = Blueprint("auth", __name__, url_prefix="/auth")




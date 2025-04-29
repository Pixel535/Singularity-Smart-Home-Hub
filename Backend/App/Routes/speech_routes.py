from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from Backend.App.Services.speech_services import generate_greeting

speech_route = Blueprint("speech", __name__)

@speech_route.route("/greet", methods=["POST"])
@jwt_required(locations=["cookies"])
def greet_route():
    data = request.get_json()
    return generate_greeting(data)

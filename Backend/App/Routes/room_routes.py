from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.App.Services.room_services import get_room_data

room_route = Blueprint("house/room", __name__)

@room_route.route("/getRoom", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_room_info():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = get_room_data(user_login, data)
    return jsonify(response), status

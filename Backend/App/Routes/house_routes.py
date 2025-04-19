from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.App.Services.house_services import get_house_data

house_route = Blueprint("house", __name__)

@house_route.route("/<int:house_id>", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_house(house_id):
    user_login = get_jwt_identity()
    response, status = get_house_data(user_login, house_id)
    return jsonify(response), status

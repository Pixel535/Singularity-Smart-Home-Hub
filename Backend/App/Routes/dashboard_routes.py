from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.App.Services.dashboard_services import get_user_houses, add_house, remove_house, edit_house
import logging

logger = logging.getLogger(__name__)
dashboard_route = Blueprint("dashboard", __name__)

@dashboard_route.route("/houses", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_houses():
    user_login = get_jwt_identity()
    response, status = get_user_houses(user_login)
    return jsonify(response), status

@dashboard_route.route("/addHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_new_house():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = add_house(user_login, data)
    return jsonify(response), status

@dashboard_route.route("/removeHouse", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def remove_existing_house():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = remove_house(user_login, data)
    return jsonify(response), status

@dashboard_route.route("/editHouse", methods=["PUT"])
@jwt_required(locations=["cookies"])
def edit_house_route():
    user = get_jwt_identity()
    house_data = request.get_json()
    response, status = edit_house(user, house_data)
    return jsonify(response), status


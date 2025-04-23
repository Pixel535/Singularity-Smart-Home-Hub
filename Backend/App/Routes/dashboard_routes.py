from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from Backend.App.Services.dashboard_services import (get_user_houses, add_house, remove_house, edit_house)
from Backend.App.Utils.session_helper import get_identity_context, log_and_message_response, Statuses

dashboard_route = Blueprint("dashboard", __name__)


@dashboard_route.route("/houses", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_houses():
    context = get_identity_context()
    if context["is_house_session"]:
        return log_and_message_response("Please log in as a user to view houses", Statuses.FORBIDDEN)

    response, status = get_user_houses()
    return jsonify(response), status



@dashboard_route.route("/addHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_new_house():
    context = get_identity_context()
    if context["is_house_session"]:
        return log_and_message_response("Please log in as a user to create a house", Statuses.FORBIDDEN)

    data = request.get_json()
    response, status = add_house(data)
    return jsonify(response), status


@dashboard_route.route("/removeHouse", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def remove_existing_house():
    context = get_identity_context()
    if context["is_house_session"]:
        return log_and_message_response("This operation is not allowed in house session. Please log in as a user.", Statuses.FORBIDDEN)

    data = request.get_json()
    response, status = remove_house(data)
    return jsonify(response), status


@dashboard_route.route("/editHouse", methods=["PUT"])
@jwt_required(locations=["cookies"])
def edit_house_route():
    house_data = request.get_json()
    response, status = edit_house(house_data)
    return jsonify(response), status

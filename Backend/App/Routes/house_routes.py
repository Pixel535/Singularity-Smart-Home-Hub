from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from Backend.App.Services.house_services import get_house_data, get_house_rooms, add_room, edit_room_data, remove_room, \
    get_users_from_house, search_users_for_house_service, add_user_to_house_service, change_user_role_service, \
    remove_user_from_house_service, change_house_pin_service, get_pending_invitations_service, \
    accept_invitation_service, reject_invitation_service
from Backend.App.Utils.camunda_caller import start_camunda
from Backend.App.Utils.camunda_task_manager import manage_tasks
from Backend.App.Utils.session_helper import Statuses

house_route = Blueprint("house", __name__)


@house_route.route("/getHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_house_post():
    data = request.get_json()
    house_id = data.get("HouseID")
    response, status = get_house_data(house_id)
    return jsonify(response), status


@house_route.route("/getRooms", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_rooms():
    data = request.get_json()
    response, status = get_house_rooms(data)
    return jsonify(response), status


@house_route.route("/addRoom", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_new_room():
    data = request.get_json()
    response, status = add_room(data)
    return jsonify(response), status


@house_route.route("/editRoom", methods=["PUT"])
@jwt_required(locations=["cookies"])
def edit_room():
    data = request.get_json()
    response, status = edit_room_data(data)
    return jsonify(response), status


@house_route.route("/removeRoom", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete_room():
    data = request.get_json()
    response, status = remove_room(data)
    return jsonify(response), status


@house_route.route("/getHouseUsers", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_house_users():
    data = request.get_json()
    response, status = get_users_from_house(data)
    return jsonify(response), status


@house_route.route("/searchUsersForHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def search_users_for_house():
    data = request.get_json()
    response, status = search_users_for_house_service(data)
    return jsonify(response), status


@house_route.route("/addUserToHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_user_to_house():
    data = request.get_json()
    response, status = add_user_to_house_service(data)
    return jsonify(response), status


@house_route.route("/changeUserRole", methods=["PUT"])
@jwt_required(locations=["cookies"])
def change_user_role():
    data = request.get_json()
    response, status = change_user_role_service(data)
    return jsonify(response), status


@house_route.route("/removeUserFromHouse", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def remove_user_from_house():
    data = request.get_json()
    response, status = remove_user_from_house_service(data)
    return jsonify(response), status


@house_route.route("/changePin", methods=["PUT"])
@jwt_required(locations=["cookies"])
def change_house_pin():
    data = request.get_json()
    response, status = change_house_pin_service(data)
    return jsonify(response), status


@house_route.route("/getInvitations", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_invitations():
    response, status = get_pending_invitations_service()
    return jsonify(response), status


@house_route.route("/acceptInvitation", methods=["POST"])
@jwt_required(locations=["cookies"])
def accept_invitation():
    data = request.get_json()
    response, status = accept_invitation_service(data)
    return jsonify(response), status


@house_route.route("/rejectInvitation", methods=["POST"])
@jwt_required(locations=["cookies"])
def reject_invitation():
    data = request.get_json()
    response, status = reject_invitation_service(data)
    return jsonify(response), status


@house_route.route("/externalData", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_external_data():
    data = request.get_json()
    city = data.get("City")
    country = data.get("Country")
    country_code = data.get("CountryCode")

    result, status = start_camunda(city=city, country=country, country_code=country_code)
    if status != Statuses.OK:
        return jsonify(result), status

    result, error = manage_tasks()
    return result, status

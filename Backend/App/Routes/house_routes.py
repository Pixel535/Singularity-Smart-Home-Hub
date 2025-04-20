from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.App.Services.house_services import get_house_data, get_house_rooms, add_room, edit_room_data, remove_room, \
    get_users_from_house

house_route = Blueprint("house", __name__)

@house_route.route("/getHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_house_post():
    user_login = get_jwt_identity()
    data = request.get_json()
    house_id = data.get("HouseID")
    response, status = get_house_data(user_login, house_id)
    return jsonify(response), status

@house_route.route("/getRooms", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_rooms():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = get_house_rooms(user_login, data)
    return jsonify(response), status


@house_route.route("/addRoom", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_new_room():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = add_room(user_login, data)
    return jsonify(response), status


@house_route.route("/editRoom", methods=["PUT"])
@jwt_required(locations=["cookies"])
def edit_room():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = edit_room_data(user_login, data)
    return jsonify(response), status


@house_route.route("/removeRoom", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete_room():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = remove_room(user_login, data)
    return jsonify(response), status


@house_route.route("/getHouseUsers", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_house_users():
    user_login = get_jwt_identity()
    data = request.get_json()
    response, status = get_users_from_house(user_login, data)
    return jsonify(response), status

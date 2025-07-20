from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Backend.Singularity_Local.App.Services.dashboard_services import update_room_service, delete_room_service, \
    create_room_service, get_all_rooms_service, get_house_service

dashboard_route = Blueprint("dashboard", __name__)

@dashboard_route.route("/getRooms", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_all_rooms():
    return get_all_rooms_service()

@dashboard_route.route("/addRoom", methods=["POST"])
@jwt_required(locations=["cookies"])
def create_room():
    data = request.get_json()
    return create_room_service(data)

@dashboard_route.route("/editRoom", methods=["PUT"])
@jwt_required(locations=["cookies"])
def update_room():
    data = request.get_json()
    return update_room_service(data)


@dashboard_route.route("/removeRoom", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete_room():
    data = request.get_json()
    return delete_room_service(data)


@dashboard_route.route("/getHouse", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_house():
    data = request.get_json()
    house_id = data.get("HouseID")
    return get_house_service(house_id)

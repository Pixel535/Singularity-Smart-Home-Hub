from flask import jsonify

from Backend.Singularity_Local.App.Models.dashboard_model import get_rooms, update_room, delete_room, create_room, \
    get_house_from_config
from Backend.Singularity_Local.App.Utils.config_helper import load_config
from Backend.Singularity_Local.App.Utils.constants import Statuses, log_and_message_response


def get_all_rooms_service():
    config = load_config()
    house_id = config.get("house_id")
    if house_id is None:
        return log_and_message_response("No house_id found in config", Statuses.BAD_REQUEST)

    rooms = get_rooms(house_id)
    return {"rooms": rooms}, Statuses.OK


def create_room_service(data):
    config = load_config()
    house_id = config.get("house_id")
    if house_id is None:
        return log_and_message_response("No house_id found in config", Statuses.BAD_REQUEST)

    name = data.get("RoomName")
    if not name:
        return log_and_message_response("Missing room name", Statuses.BAD_REQUEST)

    room_id = create_room(house_id, name)
    return jsonify({"RoomID": room_id}), Statuses.CREATED


def update_room_service(data):
    room_id = data.get("RoomID")
    room_name = data.get("RoomName")
    if not room_id or not room_name:
        return log_and_message_response("Missing RoomID or RoomName", Statuses.BAD_REQUEST)

    update_room(room_id, room_name)
    return jsonify({"msg": "Room updated"}), Statuses.OK


def delete_room_service(data):
    room_id = data.get("RoomID")
    if not room_id:
        return log_and_message_response("Missing RoomID", Statuses.BAD_REQUEST)

    delete_room(room_id)
    return jsonify({"msg": "Room deleted"}), Statuses.OK


def get_house_service(house_id):
    try:
        house_data = get_house_from_config(house_id)
        if not house_data:
            return jsonify({"msg": "House not found"}), Statuses.NOT_FOUND

        return jsonify(house_data), Statuses.OK

    except Exception as e:
        return log_and_message_response("Failed to get house data", Statuses.BAD_REQUEST, "error", e)
from flask import jsonify

from Backend.Singularity_Local.App.Models.room_model import get_room_by_id
from Backend.Singularity_Local.App.Utils.config_helper import get_identity_context
from Backend.Singularity_Local.App.Utils.constants import log_and_message_response, Statuses


def get_room_data(data):
    context = get_identity_context()

    room_id = data.get("RoomID")
    house_id = data.get("HouseID")

    if not room_id or not house_id:
        return log_and_message_response("RoomID or HouseID missing", Statuses.BAD_REQUEST)

    try:
        room = get_room_by_id(room_id)
        if not room:
            return log_and_message_response("Room not found", Statuses.NOT_FOUND)
        if str(room["HouseID"]) != house_id:
            return log_and_message_response("Room does not belong to specified house", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error retrieving room", Statuses.BAD_REQUEST, "error", e)

    if not context["is_house_session"] or context["house_id"] != house_id:
        return log_and_message_response("Access denied", Statuses.FORBIDDEN)

    return jsonify({
        "RoomID": room["RoomID"],
        "RoomName": room["RoomName"],
        "HouseID": room["HouseID"]
    }), Statuses.OK

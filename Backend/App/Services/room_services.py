from Backend.App.Models.house_model import get_room_by_id, get_user_house_by_userID_houseID
from Backend.App.Models.user_model import get_user_by_login
from Backend.App.config import log_and_message_response, Statuses


def get_room_data(user_login, data):
    room_id = data.get("RoomID")
    house_id = data.get("HouseID")

    if not room_id or not house_id:
        return log_and_message_response("RoomID or HouseID missing", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User missing", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user info", Statuses.BAD_REQUEST, "error", e)

    user_id = user.data["UserID"]

    try:
        room = get_room_by_id(room_id)
        if not room:
            return log_and_message_response("Room not found", Statuses.NOT_FOUND)
        if room.data.get("HouseID") != house_id:
            return log_and_message_response("Room does not belong to specified house", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with getting room", Statuses.BAD_REQUEST, "error", e)

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link or not link.data:
            return log_and_message_response("Access Denied", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error verifying user-house link", Statuses.BAD_REQUEST, "error", e)

    return room.data, Statuses.OK
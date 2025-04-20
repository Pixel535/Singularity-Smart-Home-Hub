from Backend.App.Models.house_model import get_house_by_user_and_house_id, get_user_house_by_userID_houseID, \
    get_rooms_by_house_id, insert_room, get_room_by_id, update_room, delete_room, get_users_assigned_to_house
from Backend.App.Models.user_model import get_user_by_login
from Backend.App.config import log_and_message_response, Statuses


def get_house_data(user_login, house_id):
    return get_house_by_user_and_house_id(user_login, house_id)


def get_house_rooms(user_login, data):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User missing", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    house_id = data.get("HouseID")
    user_id = user.data["UserID"]

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link:
            return log_and_message_response("Access denied", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with getting link between house and user", Statuses.BAD_REQUEST, "error", e)

    try:
        rooms_result = get_rooms_by_house_id(house_id)
        return {"rooms": rooms_result.data}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to get rooms", Statuses.BAD_REQUEST, exception=e)


def add_room(user_login, data):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User missing", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    house_id = data.get("HouseID")
    user_id = user.data["UserID"]

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link:
            return log_and_message_response("Access denied", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with getting link between house and user", Statuses.BAD_REQUEST, "error", e)

    room_data = {
        "HouseID": house_id,
        "RoomName": data.get("RoomName")
    }

    try:
        inserted = insert_room(room_data)
        return {"msg": "Room added", "room": inserted.data[0]}, Statuses.CREATED
    except Exception as e:
        return log_and_message_response("Failed to add room", Statuses.BAD_REQUEST, exception=e)


def edit_room_data(user_login, data):
    room_id = data.get("RoomID")
    house_id_from_request = data.get("HouseID")
    if not room_id or not house_id_from_request:
        return log_and_message_response("RoomID or HouseID missing", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User missing", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_id = user.data["UserID"]

    try:
        room = get_room_by_id(room_id)
        if not room:
            return log_and_message_response("Room not found", Statuses.NOT_FOUND)
        if room.data["HouseID"] != house_id_from_request:
            return log_and_message_response("Room doesn't belong to this house", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with getting room", Statuses.BAD_REQUEST, "error", e)

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id_from_request)
        if not link or not link.data or link.data.get("Role") != "Owner":
            return log_and_message_response("Only owner can edit room", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with link between house and user", Statuses.BAD_REQUEST, "error", e)

    try:
        update_room(room_id, data)
        return {"msg": "Room updated"}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to update room", Statuses.BAD_REQUEST, exception=e)



def remove_room(user_login, data):
    room_id = data.get("RoomID")
    house_id_from_request = data.get("HouseID")
    if not room_id or not house_id_from_request:
        return log_and_message_response("RoomID or HouseID missing", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User missing", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_id = user.data["UserID"]

    try:
        room = get_room_by_id(room_id)
        if not room:
            return log_and_message_response("Room not found", Statuses.NOT_FOUND)
        if room.data["HouseID"] != house_id_from_request:
            return log_and_message_response("Room doesn't belong to this house", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with getting room", Statuses.BAD_REQUEST, "error", e)

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id_from_request)
        if not link or not link.data or link.data.get("Role") != "Owner":
            return log_and_message_response("Only owner can delete room", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with link between house and user", Statuses.BAD_REQUEST, "error", e)

    try:
        delete_room(room_id)
        return {"msg": "Room deleted"}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to delete room", Statuses.BAD_REQUEST, exception=e)


def get_users_from_house(user_login, data):
    try:
        user = get_user_by_login(user_login)
        if not user:
            log_and_message_response("User missing", Statuses.NOT_FOUND)
            return {"users": []}, Statuses.NOT_FOUND
    except Exception as e:
        log_and_message_response("Failed to get user info", Statuses.BAD_REQUEST, "error", e)
        return {"users": []}, Statuses.BAD_REQUEST

    house_id = data.get("HouseID")
    user_id = user.data["UserID"]

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link or not link.data:
            log_and_message_response("Access denied", Statuses.FORBIDDEN)
            return {"users": []}, Statuses.FORBIDDEN
    except Exception as e:
        log_and_message_response("Access check failed", Statuses.BAD_REQUEST, "error", e)
        return {"users": []}, Statuses.BAD_REQUEST

    try:
        response = get_users_assigned_to_house(house_id)
        if not response:
            log_and_message_response("Something went wrong with receiving data", Statuses.FORBIDDEN)
            return {"users": []}, Statuses.FORBIDDEN
        data = response.data or []
    except Exception as e:
        log_and_message_response("Failed to get house users", Statuses.BAD_REQUEST, "error", e)
        return {"users": []}, Statuses.BAD_REQUEST

    users = []
    for row in data:
        user_login = row.get("User", {}).get("UserLogin")
        role = row.get("Role")
        if user_login and role:
            users.append({
                "UserLogin": user_login,
                "Role": role
            })

    return {"users": users}, Statuses.OK
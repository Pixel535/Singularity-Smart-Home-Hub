from werkzeug.security import check_password_hash, generate_password_hash

from Backend.App.Models.house_model import get_house_by_user_and_house_id, get_user_house_by_userID_houseID, \
    get_rooms_by_house_id, insert_room, get_room_by_id, update_room, delete_room, get_users_assigned_to_house, \
    delete_user_from_house, update_user_role_in_house, insert_user_into_house, get_house_pin_by_id, update_house_pin
from Backend.App.Models.user_model import get_user_by_login, search_users_by_login_or_mail
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
        if not link or not link.data or link.data.get("Role") != "Owner":
            return log_and_message_response("Only owner can add rooms", Statuses.FORBIDDEN)
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


def search_users_for_house_service(user_login, data):
    query = data.get("query")
    house_id = data.get("HouseID")

    if not query or not house_id:
        log_and_message_response("Missing search query or HouseID", Statuses.BAD_REQUEST)
        return {"results": []}, Statuses.BAD_REQUEST

    try:
        current_user = get_user_by_login(user_login)
        current_login = current_user.data["UserLogin"]

        existing = get_users_assigned_to_house(house_id)
        existing_logins = [
            row.get("Users", {}).get("UserLogin")
            for row in existing.data or []
            if row.get("Users", {}).get("UserLogin")
        ]

        results = search_users_by_login_or_mail(query)
        filtered = [
            user for user in results.data or []
            if user["UserLogin"] not in existing_logins and user["UserLogin"] != current_login
        ]

        return {"results": filtered}, Statuses.OK

    except Exception as e:
        log_and_message_response("User search failed", Statuses.BAD_REQUEST, "error", e)
        return {"results": []}, Statuses.BAD_REQUEST


def add_user_to_house_service(user_login, data):
    house_id = data.get("HouseID")
    target_login = data.get("UserLogin")
    role_data = data.get("Role")
    role = role_data.get("value") if isinstance(role_data, dict) else role_data

    if not house_id or not target_login or not role:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_id = user.data["UserID"]

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link or not link.data or link.data.get("Role") != "Owner":
            return log_and_message_response("Only owner can add users", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with link between house and user", Statuses.BAD_REQUEST, "error", e)

    try:
        new_user = get_user_by_login(target_login)
        if not new_user:
            return log_and_message_response("User to add not found", Statuses.NOT_FOUND)

        user_data = {
            "UserID": new_user.data["UserID"],
            "HouseID": house_id,
            "Role": role
        }
        insert_user_into_house(user_data)
        return {"msg": "User added"}, Statuses.CREATED
    except Exception as e:
        return log_and_message_response("Failed to add user", Statuses.BAD_REQUEST, "error", e)


def change_user_role_service(user_login, data):
    house_id = data.get("HouseID")
    target_login = data.get("UserLogin")
    new_role = data.get("NewRole")

    if not house_id or not target_login or not new_role:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        target = get_user_by_login(target_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
        if not target:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_id = user.data["UserID"]
    target_user_id = target.data["UserID"]

    if user_id == target_user_id:
        return log_and_message_response("You cannot change your own role", Statuses.FORBIDDEN)

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link or not link.data or link.data.get("Role") != "Owner":
            return log_and_message_response("Only owner can chane roles", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with link between house and user", Statuses.BAD_REQUEST, "error", e)

    try:
        response = get_users_assigned_to_house(house_id)
        if not response:
            return log_and_message_response("Something went wrong with receiving data", Statuses.FORBIDDEN)
        data = response.data or []
    except Exception as e:
        return log_and_message_response("Failed to get house users", Statuses.BAD_REQUEST, "error", e)

    if len(data) == 1:
        return log_and_message_response("You cannot change the last member's role", Statuses.FORBIDDEN)

    try:
        update_user_role_in_house(house_id, target_user_id, new_role)
        return {"msg": "Role updated"}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to update role", Statuses.BAD_REQUEST, "error", e)


def remove_user_from_house_service(user_login, data):
    house_id = data.get("HouseID")
    target_login = data.get("UserLogin")

    if not house_id or not target_login:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        target = get_user_by_login(target_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
        if not target:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_id = user.data["UserID"]
    target_user_id = target.data["UserID"]

    if user_id == target_user_id:
        return log_and_message_response("You cannot remove yourself", Statuses.FORBIDDEN)

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link or not link.data or link.data.get("Role") != "Owner":
            return log_and_message_response("Only owner can remove users", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with link between house and user", Statuses.BAD_REQUEST, "error", e)

    try:
        response = get_users_assigned_to_house(house_id)
        if not response:
            return log_and_message_response("Something went wrong with receiving data", Statuses.FORBIDDEN)
        data = response.data or []
    except Exception as e:
        return log_and_message_response("Failed to get house users", Statuses.BAD_REQUEST, "error", e)

    if len(data) == 1:
        return log_and_message_response("You cannot remove the only user", Statuses.FORBIDDEN)

    try:
        delete_user_from_house(house_id, target_user_id)
        return {"msg": "User removed"}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to remove user", Statuses.BAD_REQUEST, "error", e)


def change_house_pin_service(user_login, data):
    house_id = data.get("HouseID")
    current_pin = str(data.get("CurrentPIN", ""))
    new_pin = str(data.get("NewPIN", ""))
    confirm_pin = str(data.get("ConfirmPIN", ""))

    if not house_id or not current_pin or not new_pin or not confirm_pin:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    if new_pin != confirm_pin:
        return log_and_message_response("PINs do not match", Statuses.BAD_REQUEST)

    if not new_pin.isdigit() or len(new_pin) != 6:
        return log_and_message_response("PIN must be 6 digits", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
        user_id = user.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error fetching user", Statuses.BAD_REQUEST, "error", e)

    try:
        link = get_user_house_by_userID_houseID(user_id, house_id)
        if not link or not link.data or link.data["Role"] != "Owner":
            return log_and_message_response("Only owner can change PIN", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Access check failed", Statuses.BAD_REQUEST, "error", e)

    try:
        house = get_house_pin_by_id(house_id)
        if not house or not house.data:
            return log_and_message_response("House not found", Statuses.NOT_FOUND)
        if not check_password_hash(house.data["PIN"], current_pin):
            return log_and_message_response("Current PIN incorrect", Statuses.UNAUTHORIZED)
    except Exception as e:
        return log_and_message_response("Error validating current PIN", Statuses.BAD_REQUEST, "error", e)

    try:
        hashed_pin = generate_password_hash(new_pin)
        update_house_pin(house_id, hashed_pin)
        return log_and_message_response("PIN updated successfully", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("Failed to update PIN", Statuses.BAD_REQUEST, "error", e)
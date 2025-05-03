from flask_socketio import leave_room
from werkzeug.security import check_password_hash, generate_password_hash

from Backend.App.Models.house_model import get_house_by_user_and_house_id, get_user_house_by_userID_houseID, \
    get_rooms_by_house_id, insert_room, get_room_by_id, update_room, delete_room, get_users_assigned_to_house, \
    delete_user_from_house, update_user_role_in_house, insert_user_into_house, get_house_pin_by_id, update_house_pin, \
    get_pending_invitations_for_house
from Backend.App.Models.user_model import get_user_by_login, search_users_by_login_or_mail, insert_invitation, \
    get_pending_invitations_for_user, delete_invitation
from Backend.App.Utils.session_helper import log_and_message_response, Statuses, get_identity_context
from Backend.App.Utils.socket_instance import socketio


def get_house_data(house_id):
    return get_house_by_user_and_house_id(house_id)


def get_house_rooms(data):
    context = get_identity_context()
    house_id = data.get("HouseID")
    if not house_id:
        return log_and_message_response("HouseID missing", Statuses.BAD_REQUEST)

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
        try:
            rooms_result = get_rooms_by_house_id(house_id)
            return {"rooms": rooms_result.data}, Statuses.OK
        except Exception as e:
            return log_and_message_response("Failed to get rooms", Statuses.BAD_REQUEST, exception=e)

    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User missing", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]
        except Exception as e:
            return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

        try:
            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data:
                return log_and_message_response("Access denied", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Error with link", Statuses.BAD_REQUEST, "error", e)

        try:
            rooms_result = get_rooms_by_house_id(house_id)
            return {"rooms": rooms_result.data}, Statuses.OK
        except Exception as e:
            return log_and_message_response("Failed to get rooms", Statuses.BAD_REQUEST, exception=e)

    return log_and_message_response("Invalid session", Statuses.UNAUTHORIZED)


def add_room(data):
    context = get_identity_context()
    house_id = data.get("HouseID")
    if not house_id:
        return log_and_message_response("HouseID missing", Statuses.BAD_REQUEST)

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
        try:
            room_data = {
                "HouseID": house_id,
                "RoomName": data.get("RoomName")
            }
            inserted = insert_room(room_data)
            return {"msg": "Room added", "room": inserted.data[0]}, Statuses.CREATED
        except Exception as e:
            return log_and_message_response("Failed to add room", Statuses.BAD_REQUEST, exception=e)

    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User missing", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]
        except Exception as e:
            return log_and_message_response("Error with user Info", Statuses.BAD_REQUEST, "error", e)

        try:
            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data or link.data.get("Role") != "Owner":
                return log_and_message_response("Only owner can add rooms", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Error with link", Statuses.BAD_REQUEST, "error", e)

        try:
            room_data = {
                "HouseID": house_id,
                "RoomName": data.get("RoomName")
            }
            inserted = insert_room(room_data)
            return {"msg": "Room added", "room": inserted.data[0]}, Statuses.CREATED
        except Exception as e:
            return log_and_message_response("Failed to add room", Statuses.BAD_REQUEST, exception=e)

    return log_and_message_response("Invalid session", Statuses.UNAUTHORIZED)


def edit_room_data(data):
    context = get_identity_context()
    room_id = data.get("RoomID")
    house_id = data.get("HouseID")
    if not room_id or not house_id:
        return log_and_message_response("RoomID or HouseID missing", Statuses.BAD_REQUEST)

    try:
        room = get_room_by_id(room_id)
        if not room:
            return log_and_message_response("Room not found", Statuses.NOT_FOUND)
        if room.data["HouseID"] != house_id:
            return log_and_message_response("Room doesn't belong to this house", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with room", Statuses.BAD_REQUEST, "error", e)

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
        try:
            update_room(room_id, data)
            return {"msg": "Room updated"}, Statuses.OK
        except Exception as e:
            return log_and_message_response("Failed to update room", Statuses.BAD_REQUEST, exception=e)

    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User missing", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]
        except Exception as e:
            return log_and_message_response("Error with user Info", Statuses.BAD_REQUEST, "error", e)

        try:
            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data or link.data.get("Role") != "Owner":
                return log_and_message_response("Only owner can edit room", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Error with link", Statuses.BAD_REQUEST, "error", e)

        try:
            update_room(room_id, data)
            return {"msg": "Room updated"}, Statuses.OK
        except Exception as e:
            return log_and_message_response("Failed to update room", Statuses.BAD_REQUEST, exception=e)

    return log_and_message_response("Invalid session", Statuses.UNAUTHORIZED)


def remove_room(data):
    context = get_identity_context()

    room_id = data.get("RoomID")
    house_id = data.get("HouseID")

    if not room_id or not house_id:
        return log_and_message_response("RoomID or HouseID missing", Statuses.BAD_REQUEST)

    try:
        room = get_room_by_id(room_id)
        if not room:
            return log_and_message_response("Room not found", Statuses.NOT_FOUND)
        if room.data["HouseID"] != house_id:
            return log_and_message_response("Room doesn't belong to this house", Statuses.FORBIDDEN)
    except Exception as e:
        return log_and_message_response("Error with getting room", Statuses.BAD_REQUEST, "error", e)

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
        try:
            delete_room(room_id)
            return {"msg": "Room deleted"}, Statuses.OK
        except Exception as e:
            return log_and_message_response("Failed to delete room", Statuses.BAD_REQUEST, exception=e)

    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User missing", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]
        except Exception as e:
            return log_and_message_response("Error with user Info", Statuses.BAD_REQUEST, "error", e)

        try:
            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data or link.data.get("Role") != "Owner":
                return log_and_message_response("Only owner can delete room", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Error with link", Statuses.BAD_REQUEST, "error", e)

        try:
            delete_room(room_id)
            return {"msg": "Room deleted"}, Statuses.OK
        except Exception as e:
            return log_and_message_response("Failed to delete room", Statuses.BAD_REQUEST, exception=e)

    return log_and_message_response("Invalid session", Statuses.UNAUTHORIZED)


def get_users_from_house(data):
    context = get_identity_context()
    house_id = data.get("HouseID")
    if not house_id:
        log_and_message_response("Missing HouseID", Statuses.BAD_REQUEST)
        return {"users": []}, Statuses.BAD_REQUEST

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
            return {"users": []}, Statuses.FORBIDDEN

    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                log_and_message_response("User missing", Statuses.NOT_FOUND)
                return {"users": []}, Statuses.NOT_FOUND
            user_id = user.data["UserID"]

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
        raw = response.data or []
    except Exception as e:
        log_and_message_response("Failed to get house users", Statuses.BAD_REQUEST, "error", e)
        return {"users": []}, Statuses.BAD_REQUEST

    users = []
    for row in raw:
        user_login = row.get("User", {}).get("UserLogin")
        role = row.get("Role")
        if user_login and role:
            users.append({
                "UserLogin": user_login,
                "Role": role
            })

    log_and_message_response("Users fetched", Statuses.OK, "success")
    return {"users": users}, Statuses.OK


def search_users_for_house_service(data):
    context = get_identity_context()
    query = data.get("query")
    house_id = data.get("HouseID")

    if not query or not house_id:
        log_and_message_response("Missing search query or HouseID", Statuses.BAD_REQUEST)
        return {"results": []}, Statuses.BAD_REQUEST

    current_login = None

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
            return {"results": []}, Statuses.FORBIDDEN

    if context["is_user_session"]:
        try:
            current_user = get_user_by_login(context["user_login"])
            current_login = current_user.data["UserLogin"]
        except Exception as e:
            log_and_message_response("Failed to get current user", Statuses.BAD_REQUEST, "error", e)
            return {"results": []}, Statuses.BAD_REQUEST

    try:
        existing_result, status = get_users_from_house({"HouseID": house_id})
        if status != Statuses.OK:
            return {"results": []}, status

        existing_logins = [user["UserLogin"] for user in existing_result["users"]]

        pending_result = get_pending_invitations_for_house(house_id)
        pending_logins = [
            i["User"]["UserLogin"]
            for i in (pending_result.data or [])
            if i.get("User") and i["User"].get("UserLogin")
        ]

        results = search_users_by_login_or_mail(query)
        filtered = [
            user for user in results.data or []
            if user["UserLogin"] not in existing_logins
                             and user["UserLogin"] not in pending_logins
                             and user["UserLogin"] != current_login
        ]

        log_and_message_response("Search completed", Statuses.OK, "success")
        return {"results": filtered}, Statuses.OK

    except Exception as e:
        log_and_message_response("User search failed", Statuses.BAD_REQUEST, "error", e)
        return {"results": []}, Statuses.BAD_REQUEST


def add_user_to_house_service(data):
    context = get_identity_context()

    house_id = data.get("HouseID")
    target_login = data.get("UserLogin")
    role_data = data.get("Role")
    role = role_data.get("value") if isinstance(role_data, dict) else role_data

    if not house_id or not target_login or not role:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    if context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User not found", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]

            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data or link.data["Role"] != "Owner":
                return log_and_message_response("Only owner can invite users", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Access check failed", Statuses.BAD_REQUEST, "error", e)

    elif context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)

    try:
        target_user = get_user_by_login(target_login)
        if not target_user:
            return log_and_message_response("User to invite not found", Statuses.NOT_FOUND)

        target_user_id = target_user.data["UserID"]

        invitation_data = {
            "UserID": target_user_id,
            "HouseID": house_id,
            "Role": role,
            "SentFromHouseSession": context["is_house_session"]
        }

        if context["is_user_session"]:
            invitation_data["SenderID"] = user.data["UserID"]

        insert_invitation(invitation_data)
        socketio.emit("invitation_created", {
            "msg": "You have a new house invitation"
        }, to=f"user_{target_user_id}")
        return {"msg": "Invitation has been sent!"}, Statuses.CREATED

    except Exception as e:
        return log_and_message_response("Failed to create invitation", Statuses.BAD_REQUEST, "error", e)


def get_pending_invitations_service():
    context = get_identity_context()

    if not context["is_user_session"]:
        return log_and_message_response("Invitations are available only for user session", Statuses.FORBIDDEN)

    try:
        user = get_user_by_login(context["user_login"])
        if not user or not user.data:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)

        result = get_pending_invitations_for_user(user.data["UserID"])
        raw = result.data or []

        invitations = [{
            "InvitationID": row["InvitationID"],
            "HouseID": row["HouseID"],
            "HouseName": row["House"]["HouseName"],
            "Role": row["Role"],
            "SenderLogin": row["Sender"]["UserLogin"] if not row["SentFromHouseSession"] else None,
            "SentFromHouseSession": row["SentFromHouseSession"]
        } for row in raw]

        return {"invitations": invitations}, Statuses.OK

    except Exception as e:
        return log_and_message_response("Failed to fetch invitations", Statuses.BAD_REQUEST, "error", e)


def accept_invitation_service(data):
    context = get_identity_context()
    invitation_id = data.get("InvitationID")

    if not context["is_user_session"]:
        return log_and_message_response("Only user session can accept invitations", Statuses.FORBIDDEN)

    if not invitation_id:
        return log_and_message_response("Missing invitation ID", Statuses.BAD_REQUEST)

    try:
        user = get_user_by_login(context["user_login"])
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)

        user_id = user.data["UserID"]
        invitations = get_pending_invitations_for_user(user_id).data or []
        matching = [i for i in invitations if i["InvitationID"] == invitation_id]

        if not matching:
            return log_and_message_response("Invitation not found", Statuses.NOT_FOUND)

        invitation = matching[0]

        insert_user_into_house({
            "UserID": user_id,
            "HouseID": invitation["HouseID"],
            "Role": invitation["Role"]
        })

        delete_invitation(invitation_id)
        socketio.start_background_task(lambda: leave_room(f"user_{user_id}"))
        return {"msg": "Invitation accepted"}, Statuses.OK

    except Exception as e:
        return log_and_message_response("Failed to accept invitation", Statuses.BAD_REQUEST, "error", e)


def reject_invitation_service(data):
    context = get_identity_context()
    invitation_id = data.get("InvitationID")

    if not context["is_user_session"]:
        return log_and_message_response("Only user session can reject invitations", Statuses.FORBIDDEN)

    if not invitation_id:
        return log_and_message_response("Missing invitation ID", Statuses.BAD_REQUEST)

    try:
        delete_invitation(invitation_id)
        user_id = context["user_login"]
        socketio.start_background_task(lambda: leave_room(f"user_{user_id}"))
        return {"msg": "Invitation rejected"}, Statuses.OK

    except Exception as e:
        return log_and_message_response("Failed to reject invitation", Statuses.BAD_REQUEST, "error", e)


def change_user_role_service(data):
    context = get_identity_context()
    house_id = data.get("HouseID")
    target_login = data.get("UserLogin")
    new_role = data.get("NewRole")

    if not house_id or not target_login or not new_role:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    try:
        target = get_user_by_login(target_login)
        if not target:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
        target_user_id = target.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error fetching target user", Statuses.BAD_REQUEST, "error", e)

    if context["is_user_session"]:
        try:
            current = get_user_by_login(context["user_login"])
            if not current:
                return log_and_message_response("User not found", Statuses.NOT_FOUND)
            user_id = current.data["UserID"]

            if user_id == target_user_id:
                return log_and_message_response("You cannot change your own role", Statuses.FORBIDDEN)

            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data or link.data["Role"] != "Owner":
                return log_and_message_response("Only owner can change roles", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Access check failed", Statuses.BAD_REQUEST, "error", e)

    elif context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)

    try:
        response = get_users_assigned_to_house(house_id)
        if not response:
            log_and_message_response("Something went wrong with receiving data", Statuses.FORBIDDEN)
            return log_and_message_response("Failed to verify members", Statuses.FORBIDDEN)
        members = response.data or []
    except Exception as e:
        return log_and_message_response("Failed to get house users", Statuses.BAD_REQUEST, "error", e)

    if len(members) == 1:
        return log_and_message_response("You cannot change the last member's role", Statuses.FORBIDDEN)

    try:
        update_user_role_in_house(house_id, target_user_id, new_role)
        return {"msg": "Role updated"}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to update role", Statuses.BAD_REQUEST, "error", e)


def remove_user_from_house_service(data):
    context = get_identity_context()
    house_id = data.get("HouseID")
    target_login = data.get("UserLogin")

    if not house_id or not target_login:
        return log_and_message_response("Missing data", Statuses.BAD_REQUEST)

    try:
        target = get_user_by_login(target_login)
        if not target:
            return log_and_message_response("User not found", Statuses.NOT_FOUND)
        target_user_id = target.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error getting target user", Statuses.BAD_REQUEST, "error", e)

    if context["is_user_session"]:
        try:
            current_user = get_user_by_login(context["user_login"])
            if not current_user:
                return log_and_message_response("User not found", Statuses.NOT_FOUND)
            user_id = current_user.data["UserID"]

            if user_id == target_user_id:
                return log_and_message_response("You cannot remove yourself", Statuses.FORBIDDEN)

            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data or link.data["Role"] != "Owner":
                return log_and_message_response("Only owner can remove users", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Access check failed", Statuses.BAD_REQUEST, "error", e)

    elif context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)

    try:
        response = get_users_assigned_to_house(house_id)
        members = response.data or []
    except Exception as e:
        return log_and_message_response("Failed to get house users", Statuses.BAD_REQUEST, "error", e)

    if len(members) == 1:
        return log_and_message_response("You cannot remove the only user", Statuses.FORBIDDEN)

    try:
        delete_user_from_house(house_id, target_user_id)
        return {"msg": "User removed"}, Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to remove user", Statuses.BAD_REQUEST, "error", e)


def change_house_pin_service(data):
    context = get_identity_context()
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

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User not found", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]

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

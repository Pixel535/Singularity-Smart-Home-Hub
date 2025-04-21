from Backend.App.Models.user_model import get_user_by_login
from Backend.App.config import Config, Statuses, log_and_message_response


def get_house_by_user_and_house_id(user_login, house_id):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")
        user_id = user.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    try:
        user_house = Config.supabase.table("UserHouse").select("*").eq("UserID", user_id).eq("HouseID", house_id).maybe_single().execute()
        if not user_house or not user_house.data:
            return log_and_message_response("User has no access to this house", Statuses.FORBIDDEN, "error", None)
    except Exception as e:
        return log_and_message_response("Failed to check UserHouse link", Statuses.BAD_REQUEST, "error", e)

    try:
        house = Config.supabase.table("House").select("*").eq("HouseID", house_id).maybe_single().execute()
        if not house or not house.data:
            return log_and_message_response("House not found", Statuses.NOT_FOUND, "error", None)
        result = house.data
        result["Role"] = user_house.data["Role"]
        return result, Statuses.OK
    except Exception as e:
        return log_and_message_response("Fetching house failed", Statuses.BAD_REQUEST, "error", e)


def get_user_house_by_userID_houseID(user_id, house_id):
    try:
        return Config.supabase.table("UserHouse").select("*").eq("UserID", user_id).eq("HouseID", house_id).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Failed to verify UserHouse link", Statuses.BAD_REQUEST, "error", e)


def get_room_by_id(room_id):
    try:
        return Config.supabase.table("Room").select("*").eq("RoomID", room_id).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Failed to fetch room", Statuses.BAD_REQUEST, "error", e)


def get_rooms_by_house_id(house_id):
    try:
        return Config.supabase.table("Room").select("*").eq("HouseID", house_id).execute()
    except Exception as e:
        return log_and_message_response("Failed to fetch rooms", Statuses.BAD_REQUEST, "error", e)


def insert_room(room_data):
    return Config.supabase.table("Room").insert(room_data).execute()


def update_room(room_id, data):
    return Config.supabase.table("Room").update(data).eq("RoomID", room_id).execute()


def delete_room(room_id):
    return Config.supabase.table("Room").delete().eq("RoomID", room_id).execute()


def get_users_assigned_to_house(house_id):
    try:
        return Config.supabase.table("UserHouse").select("Role, User(UserLogin)").eq("HouseID", house_id).execute()
    except Exception as e:
        return log_and_message_response("Error while fetching users from house", Statuses.BAD_REQUEST, "error", e)

def insert_user_into_house(data):
    return Config.supabase.table("UserHouse").insert(data).execute()

def update_user_role_in_house(house_id, user_id, role):
    return Config.supabase.table("UserHouse").update({"Role": role}).eq("HouseID", house_id).eq("UserID", user_id).execute()

def delete_user_from_house(house_id, user_id):
    return Config.supabase.table("UserHouse").delete().eq("HouseID", house_id).eq("UserID", user_id).execute()

from Backend.App import Config
from Backend.App.Models.User.user_model import get_user_by_login
from Backend.App.config import log_and_message_response, Statuses


def get_houses_by_user_login(user_login):
    try:
        user = get_user_by_login(user_login)
        if not user:
            log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)
            return []
        user_id = user.data["UserID"]
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    try:
        response = Config.supabase.from_("UserHouse").select("*, House(*)").eq("UserID", user_id).execute()
    except Exception as e:
        log_and_message_response("Error with getting houses", Statuses.BAD_REQUEST, "error", e)
        return []

    return [row["House"] for row in response.data]


def insert_user_house(user_login, house_data):
    try:
        user = get_user_by_login(user_login)
        if not user or not house_data:
            return log_and_message_response("No user or House found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    country = house_data.get("Country", {})
    house_data["Country"] = country.get("name", "")
    house_data["CountryCode"] = country.get("code", "")

    try:
        house_insert = Config.supabase.table("House").insert(house_data).execute()
    except Exception as e:
        return log_and_message_response("House insertion failed", Statuses.BAD_REQUEST, "error", e)

    house_id = house_insert.data[0]["HouseID"]

    try:
        Config.supabase.table("UserHouse").insert({
            "UserID": user_id,
            "HouseID": house_id,
            "Role": "Owner"
        }).execute()
        return log_and_message_response("House added successfully", Statuses.CREATED, "success", None)
    except Exception as e:
        return log_and_message_response("House insertion failed", Statuses.BAD_REQUEST, "error", e)


def delete_user_house(user_login, house_data):
    try:
        user = get_user_by_login(user_login)
        if not user or not house_data:
            return log_and_message_response("No user or House found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
        house_id = house_data.get("HouseID")
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    if not house_id:
        return log_and_message_response("There is no such house", Statuses.NOT_FOUND, "error", None)

    user_house = get_user_house_by_userID_houseID(user_id, house_id)

    if not user_house or user_house.data["Role"] != "Owner":
        return log_and_message_response("UserHouse not found or User is not Owner", Statuses.NOT_FOUND, "error", None)

    try:
        return Config.supabase.table("House").delete().eq("HouseID", house_id).execute()
    except Exception as e:
        return log_and_message_response("House deletion failed", Statuses.BAD_REQUEST, "error", e)


def update_user_house(user_login, house_data):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
        house_id = house_data.get("HouseID")
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    if not house_id:
        return log_and_message_response("There is no such house", Statuses.NOT_FOUND, "error", None)

    user_house = get_user_house_by_userID_houseID(user_id, house_id)

    if not user_house or user_house.data["Role"] != "Owner":
        return log_and_message_response("UserHouse not found or User is not Owner", Statuses.NOT_FOUND, "error", None)

    country = house_data.get("Country", {})
    house_data["Country"] = country.get("name", "")
    house_data["CountryCode"] = country.get("code", "")

    try:
        Config.supabase.table("House").update(house_data).eq("HouseID", house_id).execute()
        return log_and_message_response("House updated successfully", Statuses.OK, "success", None)
    except Exception as e:
        return log_and_message_response("House update failed", Statuses.BAD_REQUEST, "error", e)

def get_user_house_by_userID_houseID(userID, houseID):
    try:
        return Config.supabase.table("UserHouse").select("*").eq("UserID", userID).eq("HouseID", houseID).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("UserHouse getting failed", Statuses.BAD_REQUEST, "error", e)

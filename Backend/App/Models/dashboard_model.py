from werkzeug.security import generate_password_hash
from Backend.App.config import Config
from Backend.App.Models.house_model import get_user_house_by_userID_houseID
from Backend.App.Models.user_model import get_user_by_login
from Backend.App.Utils.session_helper import log_and_message_response, Statuses, get_identity_context


def get_houses_by_user_login():
    context = get_identity_context()

    try:
        user = get_user_by_login(context["user_login"])
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

    return [
        {
            **{k: v for k, v in row["House"].items() if k != "PIN"},
            "Role": row.get("Role")
        }
        for row in response.data
    ]


def insert_user_house(house_data):
    context = get_identity_context()

    try:
        user = get_user_by_login(context["user_login"])
        if not user or not house_data:
            return log_and_message_response("No user or House found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    country = house_data.get("Country", {})
    house_data["Country"] = country.get("name", "")
    house_data["CountryCode"] = country.get("code", "")

    pin = house_data.get("PIN")
    if not pin or not str(pin).isdigit() or len(str(pin)) != 6:
        return log_and_message_response("PIN must be a 6-digit number", Statuses.BAD_REQUEST)

    house_data["PIN"] = generate_password_hash(str(pin))

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


def delete_user_house(house_data):
    context = get_identity_context()

    house_id = house_data.get("HouseID")
    if not house_id:
        return log_and_message_response("There is no such house", Statuses.NOT_FOUND, "error", None)

    try:
        user = get_user_by_login(context["user_login"])
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_house = get_user_house_by_userID_houseID(user_id, house_id)
    if not user_house or user_house.data["Role"] != "Owner":
        return log_and_message_response("UserHouse not found or User is not Owner", Statuses.NOT_FOUND, "error", None)

    try:
        Config.supabase.table("House").delete().eq("HouseID", house_id).execute()
        return log_and_message_response("House deleted", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("House deletion failed", Statuses.BAD_REQUEST, "error", e)


def update_user_house(house_data):
    context = get_identity_context()
    house_id = house_data.get("HouseID")
    if not house_id:
        return log_and_message_response("There is no such house", Statuses.NOT_FOUND, "error", None)

    country = house_data.get("Country", {})
    house_data["Country"] = country.get("name", "")
    house_data["CountryCode"] = country.get("code", "")

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)
        try:
            Config.supabase.table("House").update(house_data).eq("HouseID", house_id).execute()
            return log_and_message_response("House updated successfully", Statuses.OK, "success", None)
        except Exception as e:
            return log_and_message_response("House update failed", Statuses.BAD_REQUEST, "error", e)

    try:
        user = get_user_by_login(context["user_login"])
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_house = get_user_house_by_userID_houseID(user_id, house_id)
    if not user_house or user_house.data["Role"] != "Owner":
        return log_and_message_response("UserHouse not found or User is not Owner", Statuses.NOT_FOUND, "error", None)

    try:
        Config.supabase.table("House").update(house_data).eq("HouseID", house_id).execute()
        return log_and_message_response("House updated successfully", Statuses.OK, "success", None)
    except Exception as e:
        return log_and_message_response("House update failed", Statuses.BAD_REQUEST, "error", e)

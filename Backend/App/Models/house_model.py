from Backend.App.Models.user_model import get_user_by_login
from Backend.App.config import Statuses, log_and_message_response, Config


def get_house_by_user_and_house_id(user_login, house_id):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")
        user_id = user.data["UserID"]
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

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
        return house.data, Statuses.OK
    except Exception as e:
        return log_and_message_response("Fetching house failed", Statuses.BAD_REQUEST, "error", e)
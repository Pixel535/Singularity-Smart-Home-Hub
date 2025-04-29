from Backend.App.config import Config
from Backend.App.Utils.session_helper import log_and_message_response, Statuses


def get_country_code_for_house(house_id):
    try:
        return Config.supabase.table("House").select("CountryCode").eq("HouseID", house_id).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Failed to fetch house country code", Statuses.BAD_REQUEST, "error", e)
from Backend.Singularity_Local.App.config import Config
from Backend.Singularity_Local.App.Utils.constants import log_and_message_response, Statuses
from Backend.Singularity_Local.App.Utils.security import hash_pin


def get_house_by_id(house_id):
    try:
        return Config.supabase.table("House").select("*").eq("HouseID", house_id).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Failed to get house with given ID", Statuses.BAD_REQUEST, "error", e)

def get_houses_by_user_id_for_owners(user_id):
    try:
        return Config.supabase.from_("UserHouse").select("*, House(*)").eq("UserID", user_id).eq("Role", "Owner").execute()
    except Exception as e:
        return log_and_message_response("Failed to get houses", Statuses.BAD_REQUEST, "error", e)

def insert_user_house(user_id, house_data):
    try:
        pin = house_data.get("PIN")
        if not pin or not str(pin).isdigit() or len(str(pin)) != 6:
            return log_and_message_response("PIN must be a 6-digit number", Statuses.BAD_REQUEST)

        # Hash PIN
        pin_hash = hash_pin(pin)

        insert_data = {
            "Name": house_data["HouseName"],
            "PIN": pin_hash,
            "City": house_data["City"],
            "Country": house_data["Country"],
            "StreetAddress": house_data["StreetAddress"],
            "PostalCode": house_data["PostalCode"],
            "CountryCode": house_data["CountryCode"]
        }

        house_resp = Config.supabase.table("House").insert(insert_data).execute()
        house_id = house_resp.data[0]["HouseID"]

        Config.supabase.table("UserHouse").insert({
            "UserID": user_id,
            "HouseID": house_id,
            "Role": "owner"
        }).execute()

        return house_id, Statuses.CREATED

    except Exception as e:
        return log_and_message_response("Failed to insert house", Statuses.BAD_REQUEST, "error", e)
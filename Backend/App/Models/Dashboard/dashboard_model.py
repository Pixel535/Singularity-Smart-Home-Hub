from Backend.App import Config

def get_houses_by_user_login(user_login):
    user = Config.supabase.table("User").select("UserID").eq("UserLogin", user_login).single().execute()
    if not user.data:
        return []
    user_id = user.data["UserID"]

    response = Config.supabase.from_("UserHouse").select("*, House(*)").eq("UserID", user_id).execute()

    if response.data:
        return [row["House"] for row in response.data]
    return []

def insert_user_house(user_login, house_data):
    user = Config.supabase.table("User").select("UserID").eq("UserLogin", user_login).single().execute()
    if not user.data:
        return False
    user_id = user.data["UserID"]

    house_insert = Config.supabase.table("House").insert(house_data).execute()
    if not house_insert.data:
        return False

    house_id = house_insert.data[0]["HouseID"]

    user_house_insert = Config.supabase.table("UserHouse").insert({
        "UserID": user_id,
        "HouseID": house_id,
        "Role": "Owner"
    }).execute()

    return bool(user_house_insert.data)

def delete_user_house(user_login, house_data):
    user = Config.supabase.table("User").select("UserID").eq("UserLogin", user_login).single().execute()
    if not user.data:
        return False

    user_id = user.data["UserID"]
    house_id = house_data.get("HouseID")
    if not house_id:
        return False

    user_house = Config.supabase.table("UserHouse").select("*").eq("UserID", user_id).eq("HouseID", house_id).single().execute()

    if not user_house.data or user_house.data["Role"] != "Owner":
        return False

    Config.supabase.table("House").delete().eq("HouseID", house_id).execute()
    return True

def update_user_house(user_login, house_data):
    user = Config.supabase.table("User").select("UserID").eq("UserLogin", user_login).single().execute()
    if not user.data:
        return False

    user_id = user.data["UserID"]
    house_id = house_data.get("HouseID")
    if not house_id:
        return False

    user_house = Config.supabase.table("UserHouse").select("*").eq("UserID", user_id).eq("HouseID", house_id).single().execute()
    if not user_house.data or user_house.data["Role"] != "Owner":
        return False

    updated = Config.supabase.table("House").update(house_data).eq("HouseID", house_id).execute()
    return bool(updated.data)
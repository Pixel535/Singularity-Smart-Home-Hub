from Backend.App import Config

def get_user_by_login(login):
    try:
        return Config.supabase.table("User").select("*").eq("UserLogin", login).single().execute()
    except Exception:
        return type("Response", (object,), {"data": None})()

def get_user_by_mail(mail):
    try:
        return Config.supabase.table("User").select("*").eq("Mail", mail).single().execute()
    except Exception:
        return type("Response", (object,), {"data": None})()

def get_user_by_phone(phone):
    try:
        return Config.supabase.table("User").select("*").eq("TelephoneNumber", phone).single().execute()
    except Exception:
        return type("Response", (object,), {"data": None})()

def create_user(user_data):
    return Config.supabase.table("User").insert(user_data).execute()
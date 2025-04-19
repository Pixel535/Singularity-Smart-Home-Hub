from Backend.App import Config
from Backend.App.config import log_and_message_response, Statuses


def get_user_by_login(login):
    try:
        return Config.supabase.table("User").select("*").eq("UserLogin", login).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Getting user login failed", Statuses.BAD_REQUEST, "error", e)


def get_user_by_mail(mail):
    try:
        return Config.supabase.table("User").select("*").eq("Mail", mail).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Getting user mail failed", Statuses.BAD_REQUEST, "error", e)


def get_user_by_phone(phone):
    try:
        return Config.supabase.table("User").select("*").eq("TelephoneNumber", phone).maybe_single().execute()
    except Exception as e:
        return log_and_message_response("Getting user phone failed", Statuses.BAD_REQUEST, "error", e)


def create_user(user_data):
    return Config.supabase.table("User").insert(user_data).execute()

def update_user(user_id, data):
    return Config.supabase.table("User").update(data).eq("UserID", user_id).execute()

def delete_user(user_id):
    return Config.supabase.table("User").delete().eq("UserID", user_id).execute()

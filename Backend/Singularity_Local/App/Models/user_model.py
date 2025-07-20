from Backend.App.config import Config
from Backend.App.Utils.session_helper import log_and_message_response, Statuses


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

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


def search_users_by_login_or_mail(query):
    try:
        return Config.supabase.table("User").select("UserLogin").or_(f"UserLogin.ilike.%{query}%,Mail.ilike.%{query}%").execute()
    except Exception as e:
        return log_and_message_response("User search query failed", Statuses.BAD_REQUEST, "error", e)

def insert_invitation(data):
    return Config.supabase.table("PendingInvitation").insert(data).execute()

def get_pending_invitations_for_user(user_id):
    try:
        return Config.supabase.table("PendingInvitation").select("InvitationID, Role, HouseID, SentFromHouseSession, House(HouseName), SenderID, Sender:User!pendinginvitation_senderid_fkey(UserLogin)").eq("UserID", user_id).execute()
    except Exception as e:
        return log_and_message_response("Failed to fetch invitations", Statuses.BAD_REQUEST, "error", e)

def delete_invitation(invitation_id):
    return Config.supabase.table("PendingInvitation").delete().eq("InvitationID", invitation_id).execute()
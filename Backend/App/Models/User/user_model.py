from supabase import create_client
from Backend.App import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def get_user_by_login(login):
    return supabase.table("User").select("*").eq("UserLogin", login).single().execute()

def get_user_by_mail(mail):
    return supabase.table("User").select("*").eq("Mail", mail).single().execute()

def get_user_by_phone(phone):
    return supabase.table("User").select("*").eq("TelephoneNumber", phone).single().execute()

def create_user(user_data):
    return supabase.table("User").insert(user_data).execute()
import os
from dotenv import load_dotenv
from datetime import timedelta
from supabase import create_client

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
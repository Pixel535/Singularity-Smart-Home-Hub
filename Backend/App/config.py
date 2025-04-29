import os
from dotenv import load_dotenv
from datetime import timedelta
from supabase import create_client

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  #True na produkcji, False na http lokalnym
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/auth/refresh"
    JWT_CSRF_REFRESH_COOKIE_PATH = "/auth/refresh"
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN"
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_SESSION_COOKIE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:4200")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
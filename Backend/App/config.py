import logging
import os
from dotenv import load_dotenv
from datetime import timedelta
from supabase import create_client

load_dotenv()
logger = logging.getLogger(__name__)

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


class Statuses:
    OK = 200
    CREATED = 201

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409


def log_and_message_response(message="An error occurred", status_code=Statuses.BAD_REQUEST, response_type="error", exception=None):

    if response_type == "success":
        logger.info(f"[SUCCESS] - {message} - STATUS CODE: {Statuses.CREATED}")
    elif response_type == "info":
        logger.info(f"[INFO] - {message} - STATUS CODE: {Statuses.CONFLICT}")
    elif response_type == "error":
        if exception is None:
            logger.error(f"[ERROR] - {message} - STATUS CODE: {Statuses.UNAUTHORIZED}")
        else:
            logger.error(f"[ERROR] - {message} - STATUS CODE: {Statuses.UNAUTHORIZED}, ERROR MESSAGE: {exception}")

    return {"msg": message}, status_code
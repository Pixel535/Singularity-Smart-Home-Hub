from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies, get_csrf_token
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.App.Models.User.user_model import get_user_by_login, get_user_by_mail, get_user_by_phone, create_user
import logging

from Backend.App.config import Statuses, log_and_message_response, Config

logger = logging.getLogger(__name__)


def register_user(data):
    if get_user_by_login(data["UserLogin"]).data:
        return log_and_message_response("Login already exists", Statuses.CONFLICT, "info", None)
    if get_user_by_mail(data["Mail"]).data:
        return log_and_message_response("Email already in use", Statuses.CONFLICT, "info", None)
    if get_user_by_phone(data["TelephoneNumber"]).data:
        return log_and_message_response("Phone number already in use", Statuses.CONFLICT, "info", None)

    data["Password"] = generate_password_hash(data["Password"])

    try:
        create_user(data)
        return log_and_message_response("User created", Statuses.CREATED, "success", None)
    except Exception as e:
        return log_and_message_response("Error occured during Registering", Statuses.UNAUTHORIZED, "error", e)


def login_user(identifier, password):
    user = get_user_by_login(identifier)
    if not user.data:
        user = get_user_by_mail(identifier)
        if not user.data:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)

    if not check_password_hash(user.data["Password"], password):
        return log_and_message_response("Invalid credentials", Statuses.UNAUTHORIZED, "error", None)

    access_token = create_access_token(identity=user.data["UserLogin"])
    refresh_token = create_refresh_token(identity=user.data["UserLogin"])

    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, Statuses.OK


def refresh_token_service():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    response = jsonify({"msg": "Token refreshed"})
    set_access_cookies(response, new_access_token)
    return response, Statuses.OK


def logout_user():
    response = jsonify({"msg": "Logout successful"})
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    return response, Statuses.OK
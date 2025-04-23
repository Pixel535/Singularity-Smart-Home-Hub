from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from Backend.App.Models.house_model import get_house_pin_by_id
from Backend.App.Models.user_model import get_user_by_login, get_user_by_mail, get_user_by_phone, create_user
import logging

from Backend.App.Utils.session_helper import log_and_message_response, Statuses

logger = logging.getLogger(__name__)


def register_user(data):
    if get_user_by_login(data["UserLogin"]):
        return log_and_message_response("Login already exists", Statuses.CONFLICT, "info", None)
    if get_user_by_mail(data["Mail"]):
        return log_and_message_response("Email already in use", Statuses.CONFLICT, "info", None)
    if get_user_by_phone(data["TelephoneNumber"]):
        return log_and_message_response("Phone number already in use", Statuses.CONFLICT, "info", None)

    data["Password"] = generate_password_hash(data["Password"])

    try:
        create_user(data)
        return log_and_message_response("User created", Statuses.CREATED, "success", None)
    except Exception as e:
        return log_and_message_response("Error occured during Registering", Statuses.UNAUTHORIZED, "error", e)


def login_user(identifier, password):
    try:
        user = get_user_by_login(identifier)
        if not user:
            user = get_user_by_mail(identifier)
            if not user:
                return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)

        if not check_password_hash(user.data["Password"], password):
            return log_and_message_response("Invalid credentials", Statuses.UNAUTHORIZED, "error", None)

        identity = f"user_session:{user.data['UserLogin']}"
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        response = jsonify({"msg": "Login successful"})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response, Statuses.OK
    except Exception as e:
        return log_and_message_response("Unexpected error with login", Statuses.BAD_REQUEST, "error", e)



def refresh_token_service():
    identity = get_jwt_identity()
    if not identity or not isinstance(identity, str):
        return log_and_message_response("Invalid token", Statuses.UNAUTHORIZED)

    if not identity.startswith("user_session:") and not identity.startswith("house_session:"):
        return log_and_message_response("Unknown session type", Statuses.UNAUTHORIZED)

    new_access_token = create_access_token(identity=identity)
    response = jsonify({"msg": "Token refreshed"})
    set_access_cookies(response, new_access_token)
    return response, Statuses.OK


def logout_user():
    response = jsonify({"msg": "Logout successful"})
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    return response, Statuses.OK


def login_house_session(data):
    house_id = data.get("HouseID")
    pin = data.get("PIN")

    if not house_id or not pin:
        return log_and_message_response("HouseID and PIN required", Statuses.BAD_REQUEST)

    try:
        house = get_house_pin_by_id(house_id)
        if not house or not house.data:
            return log_and_message_response("House not found", Statuses.NOT_FOUND)
    except Exception as e:
        return log_and_message_response("Error getting PIN", Statuses.BAD_REQUEST, "error", e)

    stored_pin = house.data["PIN"]

    if not check_password_hash(stored_pin, str(pin)):
        return log_and_message_response("Invalid PIN", Statuses.UNAUTHORIZED)

    identity = f"house_session:{house_id}"
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, Statuses.OK
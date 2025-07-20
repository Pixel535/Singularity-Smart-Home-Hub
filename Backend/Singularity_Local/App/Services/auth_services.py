from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    get_jwt_identity
from flask import jsonify
from werkzeug.security import check_password_hash

from Backend.App.Models.user_model import get_user_by_mail
from Backend.Singularity_Local.App.Models.user_model import get_user_by_login
from Backend.Singularity_Local.App.Utils.config_helper import load_config
from Backend.Singularity_Local.App.Utils.constants import Statuses, log_and_message_response
from Backend.Singularity_Local.App.Utils.security import verify_pin


def login_to_house(data):
    pin = data.get("PIN")
    if not pin:
        return log_and_message_response("PIN is required", status_code=Statuses.BAD_REQUEST)

    config = load_config()
    if not config:
        return log_and_message_response("Missing config.json", status_code=Statuses.FORBIDDEN)

    pin_hash = config.get("pin_hash")
    if not pin_hash or not verify_pin(pin, pin_hash):
        return log_and_message_response("Incorrect PIN", status_code=Statuses.UNAUTHORIZED)

    house_id = config.get("house_id")
    identity = f"house_session:{house_id}"
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, Statuses.OK


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


def logout_user():
    response = jsonify({"msg": "Logout successful"})
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    return response, Statuses.OK


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

from Backend.App.Models.user_model import get_user_by_login, update_user, delete_user
from Backend.App.config import log_and_message_response, Statuses
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_profile(user_login):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    user_data = {k: v for k, v in user.data.items() if k != "Password"}
    return {"user": user_data}, Statuses.OK

def update_user_profile(user_login, new_data):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    try:
        update_user(user.data["UserID"], new_data)
        return log_and_message_response("User updated successfully", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("Failed to update user", Statuses.BAD_REQUEST, "error", e)

def delete_user_account(user_login):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    try:
        delete_user(user.data["UserID"])
        return log_and_message_response("User deleted", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("Failed to delete user", Statuses.BAD_REQUEST, "error", e)


def change_user_password(user_login, data):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")
    except Exception as e:
        log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    current = data.get("CurrentPassword")
    new = data.get("NewPassword")
    confirm = data.get("ConfirmPassword")

    if new != confirm:
        return log_and_message_response("New passwords do not match", Statuses.BAD_REQUEST, "error")

    if not check_password_hash(user.data["Password"], current):
        return log_and_message_response("Current password is incorrect", Statuses.UNAUTHORIZED, "error")

    try:
        hashed = generate_password_hash(new)
        update_user(user.data["UserID"], {"Password": hashed})
        return log_and_message_response("Password changed successfully", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("Failed to change password", Statuses.BAD_REQUEST, "error", e)
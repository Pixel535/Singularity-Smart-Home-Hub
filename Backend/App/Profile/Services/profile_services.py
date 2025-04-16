from Backend.App.Models.User.user_model import get_user_by_login, update_user, delete_user
from Backend.App.config import log_and_message_response, Statuses
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_profile(user_login):
    user = get_user_by_login(user_login)

    if not user.data:
        return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")

    user_data = {k: v for k, v in user.data.items() if k != "Password"}
    return {"user": user_data}, Statuses.OK

def update_user_profile(user_login, new_data):
    user = get_user_by_login(user_login)

    if not user.data:
        return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")

    if "Password" in new_data and new_data["Password"]:
        new_data["Password"] = generate_password_hash(new_data["Password"])
    else:
        new_data.pop("Password", None)

    try:
        update_user(user.data["UserID"], new_data)
        return log_and_message_response("User updated successfully", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("Failed to update user", Statuses.BAD_REQUEST, "error", e)

def delete_user_account(user_login):
    user = get_user_by_login(user_login)

    if not user.data:
        return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")

    try:
        delete_user(user.data["UserID"])
        return log_and_message_response("User deleted", Statuses.OK, "success")
    except Exception as e:
        return log_and_message_response("Failed to delete user", Statuses.BAD_REQUEST, "error", e)


def change_user_password(user_login, data):
    user = get_user_by_login(user_login)

    if not user.data:
        return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")

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
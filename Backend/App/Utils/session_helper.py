import logging

logger = logging.getLogger(__name__)

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

from flask_jwt_extended import get_jwt_identity

def get_identity_context():
    identity = get_jwt_identity()

    if identity.startswith("house_session:"):
        return {
            "type": "house",
            "is_house_session": True,
            "is_user_session": False,
            "house_id": int(identity.split(":")[1]),
            "user_login": None
        }
    elif identity.startswith("user_session:"):
        return {
            "type": "user",
            "is_house_session": False,
            "is_user_session": True,
            "house_id": None,
            "user_login": identity.split(":")[1]
        }
    else:
        return {
            "type": "unknown",
            "is_house_session": False,
            "is_user_session": False,
            "house_id": None,
            "user_login": identity
        }

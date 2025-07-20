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

    SERVICE_UNAVAILABLE = 503

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
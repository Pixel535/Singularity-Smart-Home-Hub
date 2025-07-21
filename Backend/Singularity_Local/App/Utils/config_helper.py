import json
import os

from flask_jwt_extended import get_jwt_identity

from Backend.Singularity_Local.App.Utils.constants import log_and_message_response, Statuses
from Backend.Singularity_Local.App.config import Config

def check_for_config() -> bool:
    return os.path.exists(Config.CONFIG_PATH)

def write_config(data: dict):
    os.makedirs(os.path.dirname(Config.CONFIG_PATH), exist_ok=True)
    with open(Config.CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_config() -> dict | None:
    if not check_for_config():
        return None
    with open(Config.CONFIG_PATH, "r") as f:
        return json.load(f)

def patch_config(patch: dict):
    try:
        config = load_config()
        if not config:
            config = {}

        config.update(patch)
        write_config(config)

    except Exception as e:
        return log_and_message_response("Failed to patch config", Statuses.BAD_REQUEST, "error", e)


def get_identity_context():
    identity = get_jwt_identity()

    if identity.startswith("house_session:"):
        return {
            "type": "house",
            "is_house_session": True,
            "is_user_session": False,
            "house_id": identity.split(":")[1],
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


def get_mqtt_credentials():
    config = load_config()
    if not config:
        return None, None
    mqtt_config = config.get("mqtt", {})

    username = mqtt_config.get("username")
    password = mqtt_config.get("password")

    if username and password:
        return username, password
    return None, None

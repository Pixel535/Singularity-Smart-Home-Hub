import json
import os
import re
import uuid

from flask import jsonify

from Backend.Singularity_Local.App.Models.house_model import get_house_by_id, get_houses_by_user_id_for_owners, \
    insert_user_house
from Backend.Singularity_Local.App.Models.user_model import get_user_by_login
from Backend.Singularity_Local.App.Services.auth_services import logout_user
from Backend.Singularity_Local.App.Utils.local_db import init_local_db
from Backend.Singularity_Local.App.Utils.security import hash_pin
from Backend.Singularity_Local.App.config import Config
from Backend.Singularity_Local.App.Services.connectivity_services import check_connection
from Backend.Singularity_Local.App.Utils.config_helper import get_identity_context, patch_config
from Backend.Singularity_Local.App.Utils.constants import Statuses, log_and_message_response


def get_initialization_status():
    config_exists = os.path.exists(Config.CONFIG_PATH)
    ping_result, _ = check_connection(Config.PING_TARGET)

    response = {
        "config_exists": config_exists,
        "online": ping_result.get("online", False)
    }

    return jsonify(response), Statuses.OK


def get_houses_by_user_login():
    context = get_identity_context()

    try:
        user = get_user_by_login(context["user_login"])
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)
        user_id = user.data["UserID"]
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    try:
        response = get_houses_by_user_id_for_owners(user_id)
    except Exception as e:
        return log_and_message_response("Error with getting houses", Statuses.BAD_REQUEST, "error", e)

    return {"houses": [
        {
            **{k: v for k, v in row["House"].items() if k != "PIN"},
            "Role": row.get("Role")
        }
        for row in response.data
    ]}, Statuses.OK


def link_existing_house(user_login, house_id):
    try:
        user = get_user_by_login(user_login)
        if not user:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error", None)

        user_config_patch = {
            "userLogin": user.data["UserLogin"],
            "name": user.data["Name"],
            "surname": user.data["Surname"],
            "mail": user.data["Mail"]
        }
        patch_config(user_config_patch)
    except Exception as e:
        return log_and_message_response("Error with getting user Info", Statuses.BAD_REQUEST, "error", e)

    try:
        house = get_house_by_id(house_id)
        if not house:
            return log_and_message_response("House not found", Statuses.NOT_FOUND, "error")

        config_data = {
            "house_id": house.data["HouseID"],
            "house_token": house.data["HouseToken"],
            "house_name": house.data["Name"],
            "pin_hash": house.data["PIN"],
            "country": house.data["Country"],
            "city": house.data["City"],
            "street": house.data["StreetAddress"],
            "postal_code": house.data["PostalCode"],
            "country_code": house.data["CountryCode"]
        }

        patch_config(config_data)
        init_local_db()
        return logout_user()

    except Exception as e:
        return log_and_message_response("Failed to link house", Statuses.BAD_REQUEST, "error", e)


def create_house_offline(data):
    try:
        import random
        from Backend.Singularity_Local.App.Utils.local_db import init_local_db

        house_id = random.randint(100000, 999999)
        house_token = str(uuid.uuid4())
        pin_hash = hash_pin(data["PIN"])

        config_data = {
            "house_id": house_id,
            "house_name": data["HouseName"],
            "pin_hash": pin_hash,
            "country": data["Country"],
            "country_code": data["CountryCode"],
            "city": data["City"],
            "street": data["StreetAddress"],
            "postal_code": data["PostalCode"],
            "house_token": house_token,
            "userLogin": None,
            "mqtt": {
                "username": data.get("mqtt", {}).get("username"),
                "password": data.get("mqtt", {}).get("password")
            }
        }

        patch_config(config_data)
        init_local_db()
        return jsonify({"msg": "House created locally"}), Statuses.OK

    except Exception as e:
        return log_and_message_response("Failed to create offline house", Statuses.BAD_REQUEST, "error", e)


def create_house_online(user_login, data):
    try:
        user = get_user_by_login(user_login)
        if not user or not user.data:
            return log_and_message_response("User not found", Statuses.NOT_FOUND, "error")

        user_id = user.data["UserID"]

        house_id, error_response = insert_user_house(user_id, data)
        if error_response:
            return error_response

        pin_hash = hash_pin(data["PIN"])
        config_patch = {
            "house_id": house_id,
            "house_name": data["HouseName"],
            "pin_hash": pin_hash,
            "country": data["Country"],
            "country_code": data["CountryCode"],
            "city": data["City"],
            "street": data["StreetAddress"],
            "postal_code": data["PostalCode"],
            "house_token": None,
            "userLogin": user_login,
            "mqtt": {
                "username": data.get("mqtt", {}).get("username"),
                "password": data.get("mqtt", {}).get("password")
            }
        }

        patch_config(config_patch)
        init_local_db()
        return jsonify({"msg": "House created in database"}), Statuses.OK

    except Exception as e:
        return log_and_message_response("Failed to create online house", Statuses.BAD_REQUEST, "error", e)
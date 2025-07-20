from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Backend.Singularity_Local.App.Services.initialization_services import link_existing_house, \
    get_houses_by_user_login, create_house_offline, create_house_online, get_initialization_status
from Backend.Singularity_Local.App.Utils.config_helper import get_identity_context
from Backend.Singularity_Local.App.Utils.constants import Statuses

initialization_route = Blueprint("initialization", __name__)

@initialization_route.route('/status', methods=['GET'])
def initialization_status():
    return get_initialization_status()


@initialization_route.route('/get-houses', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_user_houses():
    return get_houses_by_user_login()


@initialization_route.route("/link-house", methods=["POST"])
@jwt_required(locations=["cookies"])
def finalize_link():
    context = get_identity_context()
    if not context["is_user_session"]:
        return {"msg": "No user session detected"}, Statuses.UNAUTHORIZED
    data = request.get_json()
    return link_existing_house(context["user_login"], data["HouseID"])


@initialization_route.route("/create-house-offline", methods=["POST"])
def create_house_offline_route():
    data = request.get_json()
    return create_house_offline(data)


@initialization_route.route("/create-house-online", methods=["POST"])
@jwt_required(locations=["cookies"])
def create_house_online_route():
    context = get_identity_context()
    if not context["is_user_session"]:
        return {"msg": "No user session detected"}, Statuses.UNAUTHORIZED
    data = request.get_json()
    return create_house_online(context["user_login"], data)

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from Backend.App.Services.profile_services import (get_user_profile, update_user_profile, delete_user_account, change_user_password)
from Backend.App.Utils.session_helper import get_identity_context, log_and_message_response, Statuses

profile_route = Blueprint("profile", __name__)


@profile_route.route("/getProfile", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_profile():
    context = get_identity_context()

    if context["is_house_session"]:
        return log_and_message_response("This endpoint is available only for user accounts", Statuses.FORBIDDEN)

    response, status = get_user_profile()
    return jsonify(response), status


@profile_route.route("/editProfile", methods=["PUT"])
@jwt_required(locations=["cookies"])
def edit_profile():
    context = get_identity_context()

    if context["is_house_session"]:
        return log_and_message_response("This endpoint is available only for user accounts", Statuses.FORBIDDEN)

    data = request.get_json()
    response, status = update_user_profile(context["user_login"], data)
    return jsonify(response), status


@profile_route.route("/deleteProfile", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete_profile():
    context = get_identity_context()

    if context["is_house_session"]:
        return log_and_message_response("This endpoint is available only for user accounts", Statuses.FORBIDDEN)

    response, status = delete_user_account(context["user_login"])
    return jsonify(response), status


@profile_route.route("/changePassword", methods=["PUT"])
@jwt_required(locations=["cookies"])
def change_password():
    context = get_identity_context()

    if context["is_house_session"]:
        return log_and_message_response("This endpoint is available only for user accounts", Statuses.FORBIDDEN)

    data = request.get_json()
    response, status = change_user_password(context["user_login"], data)
    return jsonify(response), status

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.App.Profile.Services.profile_services import get_user_profile, update_user_profile, delete_user_account, \
    change_user_password

profile_route = Blueprint("profile", __name__)

@profile_route.route("/getProfile", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_profile():
    username = get_jwt_identity()
    response, status = get_user_profile(username)
    return jsonify(response), status

@profile_route.route("/editProfile", methods=["PUT"])
@jwt_required(locations=["cookies"])
def edit_profile():
    username = get_jwt_identity()
    data = request.get_json()
    response, status = update_user_profile(username, data)
    return jsonify(response), status

@profile_route.route("/deleteProfile", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete_profile():
    username = get_jwt_identity()
    response, status = delete_user_account(username)
    return jsonify(response), status


@profile_route.route("/changePassword", methods=["PUT"])
@jwt_required(locations=["cookies"])
def change_password():
    username = get_jwt_identity()
    data = request.get_json()
    response, status = change_user_password(username, data)
    return jsonify(response), status
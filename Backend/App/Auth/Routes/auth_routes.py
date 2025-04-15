from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.App.Auth.Services.auth_services import register_user, login_user, refresh_token_service, logout_user

auth_route = Blueprint("auth", __name__)

@auth_route.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status = register_user(data)
    return response, status

@auth_route.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status = login_user(data.get("UserLogin"), data.get("Password"))
    return response, status

@auth_route.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
def refresh():
    response, status = refresh_token_service()
    return response, status

@auth_route.route("/logout", methods=["POST"])
def logout():
    return logout_user()

@auth_route.route("/me", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_me():
    user = get_jwt_identity()
    return jsonify({"user": user}), 200

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from Backend.App.Auth.Services.auth_services import register_user, login_user, refresh_token_service

auth_route = Blueprint("auth", __name__)

@auth_route.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data)

@auth_route.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data["UserLogin"], data["Password"])

@auth_route.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return refresh_token_service()
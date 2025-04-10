from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Backend.App.Auth.Services.auth_services import register_user, login_user, refresh_token_service

auth_route = Blueprint("auth", __name__)

@auth_route.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status = register_user(data)
    return jsonify(response), status

@auth_route.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status = login_user(data.get("UserLogin"), data.get("Password"))
    return jsonify(response), status

@auth_route.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    response, status = refresh_token_service()
    return jsonify(response), status
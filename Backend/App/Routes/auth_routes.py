from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt, get_jwt_identity, decode_token
from Backend.App.Services.auth_services import register_user, login_user, refresh_token_service, logout_user, login_house_session
from Backend.App.Utils.session_helper import get_identity_context, Statuses, log_and_message_response

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
    context = get_identity_context()
    if context["is_house_session"]:
        return jsonify({"session": "house", "houseId": context["house_id"]}), Statuses.OK

    if context["is_user_session"]:
        return jsonify({"session": "user", "userLogin": context["user_login"]}), Statuses.OK

    return jsonify({"session": "unknown"}), Statuses.UNAUTHORIZED


@auth_route.route("/loginHouse", methods=["POST"])
def login_house():
    data = request.get_json()
    response, status = login_house_session(data)
    return response, status


@auth_route.route("/token", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_access_token_raw():
    try:
        token = request.cookies.get("access_token_cookie")
        if not token:
            return log_and_message_response("Token not found", Statuses.NOT_FOUND)

        decoded = decode_token(token)
        identity = decoded.get("sub")
        return jsonify({
            "access_token": token,
            "identity": identity
        }), Statuses.OK

    except Exception as e:
        return log_and_message_response("Error receiving token", Statuses.NOT_FOUND, e)

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_route = Blueprint("dashboard", __name__)

@dashboard_route.route("/dashboardInfo", methods=["GET"])
@jwt_required()
def dashboard_info():
    user = get_jwt_identity()
    return jsonify({"user": user}), 200
from flask import request, Blueprint
from flask_jwt_extended import jwt_required

from Backend.Singularity_Local.App.Services.room_dashboard_services import get_room_data

room_dashboard_route = Blueprint("roomDashboard", __name__)

@room_dashboard_route.route("/getRoom", methods=["POST"])
@jwt_required(locations=["cookies"])
def get_room_info():
    data = request.get_json()
    return get_room_data(data)
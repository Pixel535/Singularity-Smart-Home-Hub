from flask import Blueprint
from flask_jwt_extended import jwt_required

from Backend.Singularity_Local.App.Services.device_services import discover_all_devices

device_route = Blueprint("device", __name__)

@device_route.route("/search", methods=["GET"])
#@jwt_required(locations=["cookies"])
def discover_devices():
    return {"devices": discover_all_devices()}, 200

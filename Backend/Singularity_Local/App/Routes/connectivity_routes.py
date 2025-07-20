from flask import Blueprint, request
from Backend.Singularity_Local.App.config import Config
from Backend.Singularity_Local.App.Services.connectivity_services import check_connection, scan_wifi, connect_wifi

connectivity_route = Blueprint("connectivity", __name__)

@connectivity_route.route('/check', methods=['GET'])
def check_connectivity():
    return check_connection(Config.PING_TARGET)


@connectivity_route.route("/wifi/scan", methods=["GET"])
def wifi_scan():
    return scan_wifi()


@connectivity_route.route("/wifi/connect", methods=["POST"])
def wifi_connect():
    data = request.get_json()
    return connect_wifi(data)
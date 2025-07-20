import subprocess
import requests
from flask import jsonify

from Backend.Singularity_Local.App.Utils.constants import Statuses, log_and_message_response


def check_connection(target):
    try:
        response = requests.get(target, timeout=3)
        if response.status_code == 200:
            return {"online": True}, Statuses.OK
        else:
            return {"online": False}, Statuses.SERVICE_UNAVAILABLE
    except Exception as e:
        return log_and_message_response("No internet connection", status_code=Statuses.BAD_REQUEST, response_type="error", exception=e)


def scan_wifi():
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], stderr=subprocess.DEVNULL, text=True)
        ssids = set(filter(None, result.decode().split('\n')))
        return jsonify([{'ssid': ssid} for ssid in ssids]), Statuses.OK
    except Exception as e:
        return log_and_message_response("Scan failed", status_code=Statuses.BAD_REQUEST, response_type="error", exception=e)


def connect_wifi(data):
    ssid = data.get("ssid")
    password = data.get("password")

    if not ssid or not password:
        return log_and_message_response("SSID and password required", status_code=Statuses.BAD_REQUEST, response_type="error")

    try:
        subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)
        return {"msg": f"Connected to {ssid}"}, Statuses.OK
    except subprocess.CalledProcessError as e:
        return log_and_message_response("Connection failed", status_code=Statuses.BAD_REQUEST, response_type="error", exception=e)
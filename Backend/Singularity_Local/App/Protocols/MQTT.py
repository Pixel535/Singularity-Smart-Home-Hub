import json
import time
from paho.mqtt import client as mqtt_client

from Backend.Singularity_Local.App.Utils.config_helper import get_mqtt_credentials
from Backend.Singularity_Local.App.Utils.constants import log_and_message_response, Statuses

BROKER = "localhost"
PORT = 1883
USERNAME, PASSWORD = get_mqtt_credentials()

TOPICS = [
    ("zigbee2mqtt/bridge/devices", 0),
    ("homeassistant/+/+/config", 0),
    ("tasmota/discovery/#", 0),
]

_discovered_devices = []
_z2m_devices = set()
_ha_devices = set()
_tasmota_devices = set()
_connected = False


def on_connect(client, userdata, flags, rc):
    global _connected
    if rc == 0:
        _connected = True
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
    else:
        log_and_message_response("MQTT connection failed", Statuses.BAD_REQUEST, "error")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode(errors='ignore')

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return

    # Zigbee2MQTT
    if topic == "zigbee2mqtt/bridge/devices":
        for device in data:
            ieee = device.get("ieee_address") or device.get("friendly_name")
            if ieee in _z2m_devices:
                continue
            _z2m_devices.add(ieee)
            _discovered_devices.append({
                "name": device.get("friendly_name", "Zigbee Device"),
                "type": "unknown",
                "protocol": "mqtt",
                "identifier": ieee,
                "category": "sensor" if device.get("type") == "EndDevice" else "unknown",
                "extra": {
                    "vendor": device.get("vendor"),
                    "model": device.get("model"),
                    "definition": device.get("definition"),
                    "topic": f"zigbee2mqtt/{device.get('friendly_name')}"
                }
            })

    # Home Assistant MQTT discovery
    elif topic.startswith("homeassistant/") and topic.endswith("/config"):
        device_id = data.get("unique_id")
        if device_id in _ha_devices:
            return
        _ha_devices.add(device_id)
        _discovered_devices.append({
            "name": data.get("name", "HA Device"),
            "type": "unknown",
            "protocol": "mqtt",
            "identifier": device_id,
            "category": data.get("device_class", "unknown"),
            "extra": {
                "component": topic.split("/")[1],
                "state_topic": data.get("state_topic"),
                "command_topic": data.get("command_topic"),
                "device": data.get("device")
            }
        })

    # Tasmota
    elif topic.startswith("tasmota/discovery/"):
        tasmota_id = data.get("dn") or data.get("mac") or topic
        if tasmota_id in _tasmota_devices:
            return
        _tasmota_devices.add(tasmota_id)
        _discovered_devices.append({
            "name": data.get("dn", "Tasmota Device"),
            "type": "unknown",
            "protocol": "mqtt",
            "identifier": tasmota_id,
            "category": None,  # domyślnie
            "extra": {
                "topic": data.get("t"),
                "mac": data.get("mac"),
                "model": data.get("md"),
                "device_class": data.get("tp")
            }
        })


def discover_mqtt_devices(timeout=2):
    global _discovered_devices, _connected, _z2m_devices, _ha_devices, _tasmota_devices
    _discovered_devices = []
    _z2m_devices.clear()
    _ha_devices.clear()
    _tasmota_devices.clear()
    _connected = False

    client = mqtt_client.Client()

    if not USERNAME or not PASSWORD:
        log_and_message_response("MQTT credentials not found in config.json", Statuses.BAD_REQUEST, "error")
        return []

    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        log_and_message_response("MQTT connect error:", Statuses.BAD_REQUEST, "error", e)
        return []

    client.loop_start()
    time.sleep(timeout)
    client.loop_stop()

    return _discovered_devices

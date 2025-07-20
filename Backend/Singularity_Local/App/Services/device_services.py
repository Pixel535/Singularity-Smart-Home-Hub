#from Backend.Singularity_Local.App.Protocols.BLE import discover_ble_devices
from Backend.Singularity_Local.App.Protocols.HTTP import discover_http_devices
from Backend.Singularity_Local.App.Protocols.MQTT import discover_mqtt_devices
from Backend.Singularity_Local.App.Protocols.SSDP import discover_ssdp_devices
from Backend.Singularity_Local.App.Protocols.mDNS import discover_mdns_devices


def discover_all_devices():
    devices = []
    #devices += discover_mdns_devices()
    #devices += discover_ssdp_devices()
    #devices += discover_ble_devices()
    #devices += discover_http_devices()
    #devices += discover_mqtt_devices()
    return devices

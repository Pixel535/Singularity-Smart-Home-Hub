#from bluepy3.btle import Scanner, DefaultDelegate
#
#
#class ScanDelegate(DefaultDelegate):
#    def __init__(self):
#        super().__init__()
#
#
#def discover_ble_devices(timeout=5):
#    scanner = Scanner().withDelegate(ScanDelegate())
#    devices = scanner.scan(timeout)
#
#    results = []
#
#    for dev in devices:
#        device_data = {
#            "name": None,
#            "type": "unknown",
#            "protocol": "ble",
#            "identifier": dev.addr,
#            "extra": {
#                "rssi": dev.rssi,
#                "address_type": dev.addrType,
#                "advertisement_data": {}
#            }
#        }
#
#        for (adtype, desc, value) in dev.getScanData():
#            device_data["extra"]["advertisement_data"][desc] = value
#            if desc == "Complete Local Name":
#                device_data["name"] = value
#
#        if not device_data["name"]:
#            device_data["name"] = "Unknown BLE Device"
#
#        results.append(device_data)
#
#    return results

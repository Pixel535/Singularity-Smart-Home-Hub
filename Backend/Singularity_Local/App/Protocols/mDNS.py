import threading
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener

from Backend.Singularity_Local.App.Utils.constants import log_and_message_response, Statuses


class MdnsListener(ServiceListener):
    def __init__(self):
        self.devices = []

    def add_service(self, zeroconf, service_type, name):
        try:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                device = {
                    "name": name.split(".")[0],
                    "type": service_type,
                    "protocol": "mdns",
                    "identifier": info.server,
                    "port": info.port,
                    "address": ".".join(map(str, info.addresses[0])) if info.addresses else None,
                    "properties": {
                        k.decode(): v.decode(errors='ignore') for k, v in info.properties.items()
                    } if info.properties else {}
                }
                self.devices.append(device)
        except Exception as e:
            log_and_message_response("Error retrieving device", Statuses.BAD_REQUEST, "error", e)


def discover_mdns_devices(timeout=2):
    listener = MdnsListener()
    zeroconf = Zeroconf()

    service_types = [
        "_esphome._tcp.local.",
        "_googlecast._tcp.local.",
        "_hap._tcp.local.",
        "_mqtt._tcp.local.",
        "_http._tcp.local.",
        "_workstation._tcp.local."
    ]

    browsers = []
    for service in service_types:
        browsers.append(ServiceBrowser(zeroconf, service, listener))

    # czekamy na odpowiedzi
    threading.Event().wait(timeout)

    zeroconf.close()
    return listener.devices

import socket
import time
import uuid

SSDP_MCAST_ADDR = "239.255.255.250"
SSDP_PORT = 1900

M_SEARCH_MSG = (
    "M-SEARCH * HTTP/1.1\r\n"
    f"HOST: {SSDP_MCAST_ADDR}:{SSDP_PORT}\r\n"
    "MAN: \"ssdp:discover\"\r\n"
    "MX: 2\r\n"
    "ST: ssdp:all\r\n"
    "\r\n"
)

def parse_ssdp_response(data: str):
    result = {}
    lines = data.split("\r\n")
    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip().upper()] = val.strip()
    return result

def discover_ssdp_devices(timeout: float = 2.0):
    discovered = []
    seen_locations = set()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)
    sock.sendto(M_SEARCH_MSG.encode(), (SSDP_MCAST_ADDR, SSDP_PORT))

    start = time.time()
    while time.time() - start < timeout:
        try:
            data, addr = sock.recvfrom(65507)
            ip = addr[0]
            decoded = data.decode(errors="ignore")
            info = parse_ssdp_response(decoded)

            location = info.get("LOCATION")
            usn = info.get("USN", str(uuid.uuid4()))

            if location and location not in seen_locations:
                seen_locations.add(location)

                device = {
                    "name": info.get("SERVER") or info.get("ST") or "Unknown SSDP device",
                    "type": "unknown",  # możemy dodać heurystykę później
                    "protocol": "ssdp",
                    "identifier": usn,
                    "address": ip,
                    "extra": {
                        "location": location,
                        "server": info.get("SERVER"),
                        "st": info.get("ST"),
                        "usn": info.get("USN")
                    }
                }

                discovered.append(device)

        except socket.timeout:
            break
        except Exception:
            continue

    sock.close()
    return discovered

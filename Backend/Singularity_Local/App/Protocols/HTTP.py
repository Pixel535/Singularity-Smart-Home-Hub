import ipaddress
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor

from Backend.Singularity_Local.App.Utils.constants import log_and_message_response, Statuses


def get_local_cidr():
    try:
        result = subprocess.check_output(["nmcli", "-g", "IP4.ADDRESS", "device", "show"], stderr=subprocess.DEVNULL, text=True)
        lines = result.strip().split("\n")
        for line in lines:
            if "/" in line:
                return line.strip()
    except Exception as e:
        log_and_message_response("Failed to get network info", Statuses.BAD_REQUEST, "error", e)
    return None


def probe_http_device(ip):
    ports = [80, 8080, 443]
    paths = ["/", "/status", "/info"]

    for port in ports:
        for path in paths:
            try:
                url = f"http://{ip}:{port}{path}"
                resp = requests.get(url, timeout=1)
                headers = dict(resp.headers)
                try:
                    json_data = resp.json()
                    response_data = json_data
                except Exception:
                    response_data = resp.text[:200]
                return {
                    "name": headers.get("Server") or "Unknown HTTP Device",
                    "type": "unknown",
                    "protocol": "http",
                    "identifier": f"{ip}:{port}",
                    "extra": {
                        "path": path,
                        "headers": headers,
                        "response": response_data
                    }
                }
            except Exception:
                continue
    return None


def discover_http_devices():
    cidr = get_local_cidr()
    if not cidr:
        return []

    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        log_and_message_response("Invalid CIDR format.", Statuses.BAD_REQUEST, "error")
        return []

    ips = [str(ip) for ip in net.hosts()]
    results = []

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(probe_http_device, ip) for ip in ips]
        for future in futures:
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception:
                continue

    return results

import os
import socket

import requests

CONSUL_HOST = os.getenv("CONSUL_HOST", "consul")


def register(name: str, port: int) -> str:
    address = socket.gethostbyname(socket.gethostname())
    service_id = f"{name}-{address}-{port}"
    payload = {
        "Name": name,
        "ID": service_id,
        "Address": address,
        "Port": port,
        "Check": {"HTTP": f"http://{address}:{port}/health", "Interval": "10s"},
    }
    requests.put(
        f"http://{CONSUL_HOST}:8500/v1/agent/service/register", json=payload, timeout=5
    ).raise_for_status()
    return service_id


def deregister(service_id: str):
    requests.put(
        f"http://{CONSUL_HOST}:8500/v1/agent/service/deregister/{service_id}", timeout=5
    ).raise_for_status()

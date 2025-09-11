import os
import random

import requests

CONSUL_HOST = os.getenv("CONSUL_HOST", "consul")


def resolve(service_name: str) -> tuple[str, int]:
    r = requests.get(
        f"http://{CONSUL_HOST}:8500/v1/health/service/{service_name}",
        params={"passing": "true"},
        timeout=3,
    )
    r.raise_for_status()
    items = r.json()
    pick = random.choice(items)
    svc = pick["Service"]
    host = svc.get("Address") or pick["Node"]["Address"]
    port = svc["Port"]
    return host, port

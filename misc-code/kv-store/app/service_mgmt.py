"""
Module for service management including registartion with Consul.
"""
import os
import logging

import requests

LOGGER = logging.getLogger(__name__)


def register_service() -> str:
    consul_agent_url = 'http://consul-server-1:8500'
    service_name = os.getenv('SERVICE_NAME', None)
    service_id = os.getenv('SERVICE_ID', None)
    service_port = os.getenv('PORT', None)
    service_addr = service_id  # we happen to name them the same in Docker compose
    if not service_name or not service_id or not service_port:
        raise Exception("Need to define SERVICE_NAME, SERVICE_ID and PORT in env vars")

    LOGGER.info(f"Registering service {service_name} with Consul")
    consul_agent_url = "http://consul-server-1:8500"

    service_definition = {
        "Name": service_name,
        "ID": service_id,
        "Address": service_addr,
        "Port": int(service_port),
        "Check": {
            "HTTP": f"http://{service_addr}:{service_port}/health",
            "Interval": "10s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }

    res = requests.put(f"{consul_agent_url}/v1/agent/service/register", json=service_definition)
    if res.status_code == 200:
        LOGGER.info(f"Registered {service_name} with Consul")
    else:
        LOGGER.error(f"Failed to register with Consul: {res.status_code} {res.text}")

    return 'no-mode-specified'
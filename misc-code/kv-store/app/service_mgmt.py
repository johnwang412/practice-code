"""
Module for service management including registartion with Consul.
"""
import os

import requests


def register_service():
    service_name = os.getenv('SERVICE_NAME', None)
    if not service_name:
        raise Exception("SERVICE_NAME not defined")


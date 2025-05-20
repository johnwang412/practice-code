"""
Module for service management including registartion with Consul.
"""
import logging
import os
import time

import consul
import requests

LOGGER = logging.getLogger(__name__)


def _try_reg_as_primary(consul_client: consul.Consul, service_id: str, service_port: str) -> bool:
    service_name = os.getenv('SERVICE_NAME_PRIMARY', None)
    if not service_name:
        raise Exception("Need to define SERVICE_NAME_PRIMARY in env vars")

    LOGGER.info(f"Trying to register {service_id} as primary for {service_name}...")

    # 1. Obtain a lock for registring as primary
    session_id: str = consul_client.session.create(
        name=f'{service_id}-{service_name}-lock',
        behavior='release',
        ttl=10,
        lock_delay=0,
    )

    # 2. Try to acquire the lock
    lock_name = f"locks/{service_name}"
    lock_acquired: bool = consul_client.kv.put(
        key=lock_name,
        value=service_id,
        acquire=session_id,
    )
    if lock_acquired:
        LOGGER.info(f"Acquired lock {lock_name} for {service_name}: {service_id}")
    else:
        LOGGER.info(f"Could not acquire lock {lock_name} for {service_name}: {service_id}")
        return False

    if lock_acquired:
        # TODO: add logic to release the lock once we're done
        # 3. If lock is acquired, register the service
        LOGGER.info(f"Registering service {service_name} with Consul...")
        register_success: bool = consul_client.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=service_id,  # we happen to name them the same in Docker compose
            port=int(service_port),
            check={
                'http': f'http://{service_id}:{service_port}/health',
                'interval': '10s',
                'deregister_critical_service_after': '1m'
            }
        )
        if register_success:
            LOGGER.info(f"SUCCESS: Registered {service_name} with Consul")
            return True
        else:
            LOGGER.error(f"Failed to register {service_name} with Consul - API call failed")

    return False


def _reg_as_replica(consul_client: consul.Consul, service_id: str, service_port: str) -> None:
    service_name = os.getenv('SERVICE_NAME_REPLICA', None)
    if not service_name:
        raise Exception("Need to define SERVICE_NAME_REPLICA in env vars")

    register_success: bool = consul_client.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=service_id,  # we happen to name them the same in Docker compose
        port=int(service_port),
        check={
            'http': f'http://{service_id}:{service_port}/health',
            'interval': '10s',
            'deregister_critical_service_after': '1m'
        }
    )
    if not register_success:
        LOGGER.error(f"Failed to register {service_id} with {service_name} in Consul - API call failed")
        return False

    LOGGER.info(f"Registered {service_id} with {service_name} in Consul")
    return True


def register_service() -> str:
    consul_client = consul.Consul(host='consul-agent')

    service_id = os.getenv('SERVICE_ID', None)
    service_port = os.getenv('PORT', None)
    if not service_id or not service_port:
        raise Exception("Need to define SERVICE_ID and PORT in env vars")

    num_attempts = 12
    sleep_sec = 5
    while num_attempts > 0:
        try:
            if _try_reg_as_primary(consul_client, service_id, service_port):
                LOGGER.info("Registered as primary")
                return 'primary'
            # If we couldn't register as primary, then register as replica
            break
        except consul.exceptions.ConsulException as e:
            LOGGER.error(f"ConsulException: {e}")
        time.sleep(sleep_sec)
        num_attempts -= 1

    if num_attempts == 0:
        raise Exception("Consul not available - unable to register service")

    reg_success: bool = _reg_as_replica(consul_client, service_id, service_port)
    if not reg_success:
        raise Exception(f"Failed to register {service_id} with Consul - API call failed")

    return 'replica'
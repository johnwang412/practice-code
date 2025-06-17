"""
Module for service management including registartion with Consul.
"""
import logging
import os
import threading
import time
from typing import Optional

import consul

import constants

LOGGER = logging.getLogger(__name__)


class ServiceInfo:
    service_id: str
    service_port: str
    service_name_primary: str
    service_name_replica: str

    def __init__(self, service_id: str, service_port: str, service_name_primary: str, service_name_replica: str):
        if None in [
            service_id,
            service_port,
            service_name_primary,
            service_name_replica
        ]:
            raise ValueError('Missing required service info')

        self.service_id = service_id
        self.service_port = service_port
        self.service_name_primary = service_name_primary
        self.service_name_replica = service_name_replica
        # If the service instance is running as primary, session_id will be populated
        self.session_id = None

    def primary_lock_name(self) -> str:
        return f'lock/{self.service_id}-{self.service_name_primary}-lock'

    def session_name(self) -> str:
        return f'{self.service_id}-{self.service_name_primary}-session'

    def set_session_id(self, session_id: str):
        self.session_id = session_id

def _get_service_info() -> dict:
    si = ServiceInfo(
        service_id=os.getenv('SERVICE_ID', None),
        service_port=os.getenv('PORT', None),
        # Name to register primary service as under Consul
        service_name_primary=os.getenv('SERVICE_NAME_PRIMARY', None),
        # Name to register replica service as under Consul
        service_name_replica=os.getenv('SERVICE_NAME_REPLICA', None)
    )
    return si


reg_service_config = {
    # monitor thread interval for checking if registration thread is alive
    'monitor_interval_sec': 10,
    # primary interval for performing operations
    'reg_primary_interval_sec': 10,
    # replica interval for performing operations
    'reg_replica_interval_sec': 5,
}


def _get_sleep_interval(app_mode: str) -> int:
    if app_mode == constants.APP_MODE_PRIMARY:
        return reg_service_config['reg_primary_interval_sec']
    elif app_mode == constants.APP_MODE_REPLICA:
        return reg_service_config['reg_replica_interval_sec']
    else:
        raise Exception(f"Invalid app mode: {app_mode}")


def _try_register_as_primary(
        consul_client: consul.Consul, service_info: ServiceInfo) -> Optional[str]:
    """
    :return: Session id if primary registration was successful, else None
    """
    # Try to acquire the primary lock
    # behavior='release' will release locks associated with the session if
    #   it's destroyed / expires
    # ttl means session will take 5 seconds more to expire than the refresh
    #   interval run by the primary node so we can be safe
    # Lock delay prevents locks from being acquired for 15s to give leader
    #   (potentially still alive) time to respond / mitigate
    session_id = consul_client.session.create(
        name=service_info.session_name(),
        behavior='release',
        ttl=reg_service_config['reg_primary_interval_sec'] + 5,
        lock_delay=15,
    )
    lock_acquired = consul_client.kv.put(
        key=service_info.primary_lock_name(),
        value=service_info.service_id,
        acquire=session_id,
    )
    if lock_acquired:
        """
        TODO: What if we acquire the lock, but fail immediately, then reboot
            and initiate another session to try and get the same lock?
            - If we succeed and get the lock, then we can proceed as before
            - If we fail, we'll keep looping as a replica until the original
                session expires
        """
        # If we were able to acquire the lock, then the primary node is down
        LOGGER.info(f"Replica {service_info.service_id} acquired lock, promoting to primary")
        # Register as primary
        # TODO: check these parameters make sense for various conditions
        register_success = consul_client.agent.service.register(
            name=service_info.service_name_primary,
            service_id=service_info.service_id,
            address=service_info.service_id,
            port=int(service_info.service_port),
            check={
                'http': f'http://{service_info.service_id}:{service_info.service_port}/health',
                'interval': '10s',
                'deregister_critical_service_after': '1m'
            }
        )
        """
        If we crash out here, we've registered as primary to Consul but we'll
        be running as replica on boot. KV store users will get forwarded to us
        so we should reject all writes if we're a replica.
        TODO: when a replica boots up, can it (should it) check if it used to
            be the primary?
        """
        if register_success:
            # Note: If this node was a replica, we don't have to deregister it
            # from the replica service group because a service_id can only be
            # registered to a single service in Consul
            LOGGER.info(f"Promoted {service_info.service_id} to primary")
            return session_id

        LOGGER.error(f"Failed to register {service_info.service_id} as primary after acquiring lock")
        return None


def _no_primary(consul_client, service_info):
    """Check the kv representing the lock on the primary node. While the
    primary node is active, it'll continue renewing its session and keep the
    lock active and bound to it's session id. There is no primary node if:
        1. The kv doesn't exist (info is None)
        2. The kv isn't associated with a session id (session has expired)
    """
    tup = consul_client.kv.get(service_info.primary_lock_name())
    lock_info: Optional[dict] = tup[1]

    if lock_info is None or 'Session' not in lock_info:
        return True
    return False


def _run_primary_configs(consul_client: consul.Consul, service_info: ServiceInfo):
    """
    TODO: Get the latest replica list
      [ ] How to do this more dynamically (same for replicas getting primary)... but does that even matter
    """
    consul_client.session.renew(session_id=service_info.session_id)


def _run_replica_configs(consul_client: consul.Consul, service_info: ServiceInfo) -> str:
    """
    TODO: Get the latest primary
    We're running as replica
    1. See if primary lock is available, if so, try to elevate to primary
      a. Try to acquire the lock - if cannot acquire, continue
      b. If acquired, de-register as replica (if needed), register as primary,
          update app_config mode
    2. If lock is not available, do nothing (already registered as replica)
    Returns the new app mode: 'primary' if promoted, else 'replica'

    Cases:
    - Initial boot up - need to register as replica if primary is already taken
    - Primary active - ensure still registered as replica (maybe no-op)
    - Primary down - try to register as primary - deregister as replica (if registered)
    """
    # resulting_app_mode represents the app mode after this fn is complete
    resulting_app_mode = constants.APP_MODE_REPLICA


    if _no_primary(consul_client, service_info):
        session_id = _try_register_as_primary(consul_client, service_info)
        if session_id is not None:
            service_info.set_session_id(session_id)
            resulting_app_mode = constants.APP_MODE_PRIMARY

    # if we're the replica, we should register as such
    if resulting_app_mode == constants.APP_MODE_REPLICA:
        # Try to re-register as replica to avoid being unregistered
        consul_client.agent.service.register(
            name=service_info.service_name_replica,
            service_id=service_info.service_id,
            address=service_info.service_id,
            port=int(service_info.service_port),
            check={
                'http': f'http://{service_info.service_id}:{service_info.service_port}/health',
                'interval': '10s',
                'deregister_critical_service_after': '1m'
            }
        )

    return resulting_app_mode


def service_registration_thread(app_config):
    """
    :param app_config: dictionary specifying the app 'mode' - to be modified
        by the service registration thread as needed
    """
    consul_client = consul.Consul(host='consul-agent')

    service_info: ServiceInfo = _get_service_info()

    while True:
        # IF app_config is primary, then do primary activities, else do replica activities
        if app_config['mode'] == constants.APP_MODE_PRIMARY:
            _run_primary_configs(consul_client, service_info)
        elif app_config['mode'] == constants.APP_MODE_REPLICA:
            app_config['mode'] = _run_replica_configs(consul_client, service_info)

        # Sleep for a while before checking again
        time.sleep(_get_sleep_interval(app_config['mode']))


def start_service_registration_thread(app_config: dict):
    """Run the daemon that spawns and respawns the registration thread
    :param app_config: dictionary specifying the app 'mode' - to be modified
        by the service registration thread as needed
    """
    def monitor_registration_thread(check_interval_sec, app_config):
        t = None
        while True:
            if not t or not t.is_alive():
                t = threading.Thread(
                    target=service_registration_thread,
                    daemon=True,
                    args=(app_config,))
                t.start()
                LOGGER.warning("Service registration thread died. Restarting...")
            time.sleep(check_interval_sec)

    monitor_interval_sec = 10
    monitor_thread = threading.Thread(
        target=monitor_registration_thread,
        daemon=True,
        args=(monitor_interval_sec, app_config))
    monitor_thread.start()
    return monitor_thread


#### OLD CODE ####

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
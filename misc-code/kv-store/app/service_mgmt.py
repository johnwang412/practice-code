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

    def __init__(self, service_id: str, service_port: str, service_name_primary: str, service_name_replica: str):
        if '' in [
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
        return f'lock/{self.service_name_primary}-lock'

    def session_name(self) -> str:
        return f'{self.service_id}-{self.service_name_primary}-session'

    def set_session_id(self, session_id: str):
        self.session_id = session_id

def _get_service_info() -> ServiceInfo:
    si = ServiceInfo(
        service_id=os.getenv('SERVICE_ID', ''),
        service_port=os.getenv('PORT', ''),
        # Name to register primary service as under Consul
        service_name_primary=os.getenv('SERVICE_NAME_PRIMARY', ''),
        # Name to register replica service as under Consul
        service_name_replica=os.getenv('SERVICE_NAME_REPLICA', '')
    )
    return si


reg_service_config = {
    # monitor thread interval for checking if registration thread is alive
    'monitor_interval_sec': 10,
    # primary interval for performing operations
    'reg_primary_interval_sec': 10,
    # replica interval for performing operations
    'reg_replica_interval_sec': 5,
    # if the primary lock is released (session expiration), how many seconds
    # until another node can acquire it
    'consul_primary_lock_delay_sec': 5,
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
    """Try to become the primary
    First acquire lock for primary node. Even if lock is acquired, ensure we
    are registered as primary service before returning session_id signifying
    we are the primary.
    If lock acquired and register call to Consul does not succeed, we continue
    acting as a replica. We shouldn't be getting traffic in that case anyways.

    :return: Session id if primary registration was successful, else None
    """
    # Try to acquire the primary lock
    # behavior='release' will release locks associated with the session if
    #   it's destroyed / expires
    # ttl means session will take 5 seconds more to expire than the refresh
    #   interval run by the primary node so we can be safe
    # Lock delay prevents locks from being acquired for X seconds to give
    #   leader (potentially still alive) time to respond / mitigate
    session_id = consul_client.session.create(
        name=service_info.session_name(),
        behavior='release',
        ttl=reg_service_config['reg_primary_interval_sec'] + 5,
        lock_delay=reg_service_config['consul_primary_lock_delay_sec'],
    )
    lock_acquired = consul_client.kv.put(
        key=service_info.primary_lock_name(),
        value=service_info.service_id,
        acquire=session_id,
    )
    if lock_acquired:
        """
        If we acquire the lock, but fail immediately and reboot, we will
        init as a replica. Replica will init another session which will
        try to get the lock, but the lock will be taken by the previous
        orphaned session and will free up once that session expires.
        """
        # If we were able to acquire the lock, then the primary node is down
        # 1. Deregister anything as the primary service
        res = consul_client.health.service(service_info.service_name_primary)
        if res[1]:
            LOGGER.info(f'Deregistering old primary service_ids...')
            for d in res[1]:
                sid = d['Service']['ID']
                dereg_res = consul_client.agent.service.deregister(sid)
                LOGGER.info(f' > deregistered {sid} with result: {dereg_res}')

        # 2. Register as primary
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
        """
        if register_success:
            # Note: If this node was a replica, we don't have to deregister it
            # from the replica service group because a service_id can only be
            # registered to a single service in Consul
            return session_id

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


def _get_nodes(consul_client: consul.Consul, service_info: ServiceInfo) -> tuple[str, list[str]]:
    """Get the list of nodes registered as primary and replicas
    :return: (primary_node_id, [replica_node_ids])
    """
    primary_node_id = None
    replica_node_ids = []

    # Get primary node
    res = consul_client.health.service(service_info.service_name_primary)
    if res[1]:
        primary_node_id = res[1][0]['Service']['ID']

    # Get replica nodes
    res = consul_client.health.service(service_info.service_name_replica)
    if res[1]:
        for d in res[1]:
            replica_node_ids.append(d['Service']['ID'])

    return primary_node_id, replica_node_ids


def _run_primary_configs(consul_client: consul.Consul, service_info: ServiceInfo) -> bool:
    """
    """
    try:
        consul_client.session.renew(session_id=service_info.session_id)
        LOGGER.info(f'Renewed session: {service_info.session_id}')
        return True
    except Exception as e:
        LOGGER.error(f'Exception renewing session ({service_info.session_id}): {e}')
    return False


def _run_replica_configs(consul_client: consul.Consul, service_info: ServiceInfo) -> str:
    """
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
        LOGGER.info(f'Attempting to register as primary')
        session_id = _try_register_as_primary(consul_client, service_info)
        if session_id is not None:
            # Set session id so we can continue to renew it
            service_info.set_session_id(session_id)
            resulting_app_mode = constants.APP_MODE_PRIMARY
            LOGGER.info(f'Set node as primary')

    # if we're the replica, we should register as such
    if resulting_app_mode == constants.APP_MODE_REPLICA:
        # Try to re-register as replica to avoid being unregistered
        res = consul_client.agent.service.register(
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
        if not res:
            LOGGER.info(f'Failed to register service id ({service_info.service_id}) as replica. Will retry next interval.')
        else:
            LOGGER.info(f'Set node as replica')

    return resulting_app_mode


def service_registration_thread(app_config):
    """
    :param app_config: dictionary specifying the app 'mode' - to be modified
        by the service registration thread as needed
    """
    consul_client = consul.Consul(host='consul-agent')
    service_info: ServiceInfo = _get_service_info()

    while True:
        try:
            # IF app_config is primary, then do primary activities, else do replica activities
            if app_config['mode'] == constants.APP_MODE_PRIMARY:
                is_primary = _run_primary_configs(consul_client, service_info)
                if not is_primary:
                    # Failed to renew session, so reverting to replica
                    app_config['mode'] = constants.APP_MODE_REPLICA
                    service_info.set_session_id(None)
            elif app_config['mode'] == constants.APP_MODE_REPLICA:
                app_config['mode'] = _run_replica_configs(consul_client, service_info)
            primary, replicas = _get_nodes(consul_client, service_info)
            app_config['primary'] = primary
            app_config['replicas'] = replicas
        except Exception as e:
            LOGGER.error(e)

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

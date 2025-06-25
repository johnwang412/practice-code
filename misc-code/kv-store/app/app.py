import json
import logging

import flask
# uwsgi is not available outside of the uwsgi server environment so skip check
import uwsgi # type: ignore
import uwsgidecorators

import kv_store
import service_mgmt
import constants

LOGGER = logging.getLogger(__name__)


# App configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
app = flask.Flask(__name__)
GLOBAL_STORE = kv_store.KVStore()
# APP_CONFIG is a heap config structure shared between main worker thread and
# the service registration thread.
APP_CONFIG = {
    'mode': constants.APP_MODE_REPLICA, # Start each node off as a replica
}


@uwsgidecorators.postfork
def post_fork_hook():
    """This function runs in the forked worker process, not in the master
    The worker process starts a thread that interfaces with Consul and
    registers the worker as either the primary or a replica.
    """
    if uwsgi.worker_id() > 0:  # Only in worker processes, not master
        service_mgmt.start_service_registration_thread(APP_CONFIG)


# APIs
@app.route('/get', methods=['GET'])
def get():
    key = flask.request.args.get('key')
    val = GLOBAL_STORE.get(key)
    if val is None:
        return '', 404
    return str(val), 200


@app.route('/put', methods=['PUT'])
def put():
    """
    TODO: reject writes if we're running in replica mode
    TODO: when replicating writes to replicas, do not replicate to self
        in case self is in the list of replicas
    """
    global GLOBAL_STORE

    data = flask.request.get_json()
    key = data.get('key')
    val = data.get('value')
    GLOBAL_STORE.put(key, val)

    ret_info = {}
    return json.dumps(ret_info), 200


@app.route('/health', methods=['GET'])
def health():
    return f'OK - mode: {APP_CONFIG["mode"]}', 200

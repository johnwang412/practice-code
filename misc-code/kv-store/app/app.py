import gc
import json
import logging
import os

import flask
import requests

import kv_store
import service_mgmt

LOGGER = logging.getLogger(__name__)


# App configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
app = flask.Flask(__name__)
GLOBAL_STORE = kv_store.KVStore()
SERVICE_MODE = service_mgmt.register_service()


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
    global GLOBAL_STORE

    data = flask.request.get_json()
    key = data.get('key')
    val = data.get('value')
    GLOBAL_STORE.put(key, val)

    ret_info = {}
    return json.dumps(ret_info), 200


@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

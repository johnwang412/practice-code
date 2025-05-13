import json
import logging
import os

import flask
from pympler import asizeof

import kv_store

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

app = flask.Flask(__name__)
global_store = kv_store.KVStore()


@app.route('/get', methods=['GET'])
def get():
    key = flask.request.args.get('key')
    val = global_store.get(key)
    if val is None:
        return '', 404
    return str(val), 200


@app.route('/put', methods=['PUT'])
def put():
    global global_store
    data = flask.request.get_json()
    key = data.get('key')
    val = data.get('value')
    global_store.put(key, val)
    ret_info = {
        'kv_store_size': asizeof.asizeof(global_store),
    }
    return json.dumps(ret_info), 200


@app.route('/harikari', methods=['POST'])
def harikari():
    raise Exception("I sacrifice myself for the greater good.")


@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

import gc
import json
import logging
import os

import flask
import requests

import kv_store

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

app = flask.Flask(__name__)
global_store = kv_store.KVStore()


def _try_peers(key):
    peer_backends = os.environ.get('BACKENDS', '').split(',')
    if peer_backends[0] == '':
        peer_backends = []
    LOGGER.info(f"Trying peers for key {key}: {peer_backends}")
    for peer in peer_backends:
        try:
            url = f'http://{peer}/peer-get?key={key}'
            response = requests.get(url, timeout=0.05)
            LOGGER.info(f"Trying peer {peer} for key {key} - response: {response.status_code}")

            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            LOGGER.error(f"Error contacting peer {peer}: {e}")
    return None


@app.route('/peer-get', methods=['GET'])
def peer_get():
    key = flask.request.args.get('key')
    val = global_store.get(key)
    if val is None:
        return '', 404
    return str(val), 200


@app.route('/get', methods=['GET'])
def get():
    key = flask.request.args.get('key')
    val = global_store.get(key)
    if val is None:
        val = _try_peers(key)
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

    ret_info = {}
    return json.dumps(ret_info), 200


@app.route('/harikari', methods=['POST'])
def harikari():
    for i in range(128):
        key = f"key_{i}"
        val = os.urandom(1024 * 1024)
        global_store.put(key, val)
    return 'OK', 200


@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

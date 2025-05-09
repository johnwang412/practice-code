import flask

import kv_store

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
    key = flask.request.args.get('key')
    val = flask.request.args.get('value')
    global_store.put(key, val)
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
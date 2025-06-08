"""
Catalog management service API

Sits within bounded context of:
- Books / Items
- Checkouts
"""
from flask import Flask, jsonify, request

from app.database import database_conn
from app.data import catalog_data

app = Flask(__name__)

@app.route('/checkout', methods=['PUT'])
def checkout_item():
    item_id = request.args.get('item_id')
    user_id = request.args.get('user_id')

    with database_conn.get_db_session() as db_session:

        success, err = catalog_data.try_checkout(item_id, user_id)

        return jsonify({
            'success': success,
            'err': err
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
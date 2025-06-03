"""
Catalog management service API

Sits within bounded context of:
- Books / Items
- Checkouts
"""
from flask import Flask, jsonify, request

from app.database import database_conn

app = Flask(__name__)

@app.route('/checkout', methods=['PUT'])
def checkout_item():
    item_id = request.args.get('item_id')
    user_id = request.args.get('user_id')

    catalog_db = database_conn.get_catalog_db()

    success, err = catalog_db.try_checkout(item_id, user_id)

    response_code = 200 if success else 500
    return jsonify({
        'success': success,
        'err': err
    }), response_code

if __name__ == '__main__':
    app.run(debug=True)
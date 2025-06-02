from flask import Flask, jsonify, request

from app.logic import catalog_management_logic
from app.database import database_conn

app = Flask(__name__)

@app.route('/checkout', methods=['PUT'])
def checkout_item():
    item_id = request.args.get('item_id')
    user_id = request.args.get('user_id')

    catalog_db = database_conn.get_catalog_db_conn()
    success, err = catalog_management_logic.checkout_item(
        catalog_db, item_id, user_id)

    response_code = 200 if success else 500
    return jsonify({
        'success': success,
        'err': err
    }), response_code

if __name__ == '__main__':
    app.run(debug=True)
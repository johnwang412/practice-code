from flask import Flask, jsonify

from app.api import user_api

flask_app = Flask(__name__)


@flask_app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


user_api.add_routes(flask_app)
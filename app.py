from flask import Flask, request, abort, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

import os

SWAGGER_URL = '/swagger'
API_URL = '/static/schema.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "users"
    }
)


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        print("In testing mode")

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


    @app.route('/ping')
    def ping():
        return jsonify(ping='pong')

    @app.route("/hello", methods=["GET", "POST"])
    def hello():
        if request.method == "GET":
            return "Hello world!"
        else:
            try:
                data = request.get_json()
                print(f"data: {data}")
                return f"Hello {data['name']}"
            except:
                abort(400, "blah")

    return app



if __name__ == "__main__":
    app = create_app()
    app.run()



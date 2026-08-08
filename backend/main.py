from flask import Flask, jsonify
from flask_restful import Api
from config import DevelopmentConfig
from extensions import init_extensions
from controllers import create_api_blueprint, register_resources


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_extensions(app)

    api_bp = create_api_blueprint()
    api = Api(api_bp)
    register_resources(api)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return jsonify({"message": "ClubSync API is running."}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask
from routes.controller import default_controller
from config.settings import Config


def create_unit_test_app():
    app = Flask(Config.APPLICATION_NAME)
    app.config.from_object(Config)
    app.register_blueprint(default_controller)

    @app.route("/", methods=["GET"])
    def health():
        return ("Healthy", 200)  
    
    return app



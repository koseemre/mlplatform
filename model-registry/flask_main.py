from flask import Flask
from routes.controller import default_controller
from config.settings import Config
import logging, os
from logging.handlers import RotatingFileHandler
from prometheus_flask_exporter import PrometheusMetrics

from flasgger import Swagger

def create_app():
    app = Flask(Config.APPLICATION_NAME)
    app.config.from_object(Config)
    app.register_blueprint(default_controller)

    # create a prometheus metrics
    prom_metrics = PrometheusMetrics(app)
    prom_metrics.info('app_info', 'model-registry', version='1.0')

    # create a log file
    handler = RotatingFileHandler(os.path.join(Config.LOG_FILE_PATH, 'model_registry.log'), maxBytes=10^6, backupCount=1)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
        
    return app, prom_metrics


app, prom_metrics = create_app()
print("Application Name:", app.name)

@app.route("/", methods=["GET"])
def health():
    """
    This function returns the health of the application.
    ---
    tags:
        - Healthcheck
    responses:
        200:
            description: The application is healthy.
            schema:
                type: string
    """    
    return ("Healthy", 200)

swagger = Swagger(app)

@app.route('/metrics')
def metrics():
    return prom_metrics.export()

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=8080)
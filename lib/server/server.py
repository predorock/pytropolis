from flask import Flask

from lib.configuration.una_config import configuration_setup

# Blueprints
from lib.blueprints.core import core
from lib.blueprints.swagger import swaggerui_blueprint, SWAGGER_URL
from lib.blueprints.runner import runner_bp
from lib.blueprints.queue import queue_bp
from lib.blueprints.stream import steam_bp
from lib.blueprints.venv import venv_bp

def create_server():
    app = Flask(__name__)
    app.register_blueprint(core)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(runner_bp)
    app.register_blueprint(queue_bp)
    app.register_blueprint(steam_bp)
    app.register_blueprint(venv_bp)

    app.shell_context_processor({"app": app})

    return app
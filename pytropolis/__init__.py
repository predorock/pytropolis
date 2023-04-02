import os
from flask import Flask

# Blueprints
from pytropolis.blueprints.core import core
from pytropolis.blueprints.swagger import swaggerui_blueprint, SWAGGER_URL
from pytropolis.blueprints.runner_bp import runner_bp
from pytropolis.blueprints.stream import steam_bp
from pytropolis.blueprints.venv import venv_bp

def create_server():
    app = Flask(__name__,
                static_folder=os.path.join(os.getcwd(), "static"),
                template_folder=os.path.join(os.getcwd(), "templates"))
    app.register_blueprint(core)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(runner_bp)
    app.register_blueprint(steam_bp)
    app.register_blueprint(venv_bp)

    app.shell_context_processor({"app": app})

    if app.debug:
        print(app.url_map)

    return app
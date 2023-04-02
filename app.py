# app.py
import redis
from flask.cli import FlaskGroup
from rq import Connection, Worker
import os

from pytropolis.server.server import create_server
from pytropolis.configuration import configuration_setup
from pytropolis.runner.venv import create_or_get_virtualenv_path


"""
    Swagger generation need an attribute that contains the Flask application.
    But the Flask application is created in the create_app function with the FlaskGroup.
    So I create a function that returns the Flask application and I pass it to the FlaskGroup in order to make everyone happy.
"""
server = create_server()
def create_for_group():
    return server


cli = FlaskGroup(create_app=create_for_group)

def init_venv(cfg):
    if not os.path.exists(cfg['venv_default']):
        create_or_get_virtualenv_path(cfg['venv_container'], 'default')

@cli.command("run_worker")
def run_worker():

    cfg = configuration_setup()
    redis_connection = redis.from_url(cfg['redis_url'])
    with Connection(redis_connection):
        worker = Worker(queues=[cfg['execution_queue']])
        worker.work()

if __name__ == "__main__":
    cfg = configuration_setup()
    init_venv(cfg)
    cli()
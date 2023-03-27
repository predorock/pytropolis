# app.py
import redis
from flask.cli import FlaskGroup
from rq import Connection, Worker
import os

from lib.server.server import create_server
from lib.configuration.una_config import configuration_setup
from lib.runner.una_runner import create_or_get_virtualenv_path


app = create_server()
cli = FlaskGroup(create_app=create_server)

def init_venv(cfg):
    if not os.path.exists(cfg['venv_default']):
        create_or_get_virtualenv_path(cfg['venv_container'], 'default')

@cli.command("run_worker")
def run_worker():

    cfg = configuration_setup()
    redis_connection = redis.from_url(cfg['redis_url'])
    with Connection(redis_connection):
        worker = Worker(queues=['una_queue'])
        worker.work()

if __name__ == "__main__":
    cfg = configuration_setup()
    init_venv(cfg)
    cli()
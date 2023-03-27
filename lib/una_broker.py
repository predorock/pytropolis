from rq import Queue
from rq.job import Job
import redis
import json
import uuid

from .configuration.una_config import get_configuration

__redis_conn = None
__redis_publisher = None

def connection_init():
    # This function initializes redis and the queue
    global __redis_conn
    global __redis_publisher
    cfg = get_configuration()
    connection_pool = redis.ConnectionPool(host=cfg['redis_host'], port=cfg['redis_port'], db=cfg['redis_db'])
    __redis_conn = redis.Redis(connection_pool=connection_pool)
    __redis_publisher = redis.StrictRedis(host=cfg['redis_host'], port=cfg['redis_port'], db=cfg['redis_db'])

def get_subscriber():
    return __redis_conn

def get_publisher():
    return __redis_publisher

def create_message(script_path, requirements_path, venv_name, execution_dir, execution_id=uuid.uuid4()):
    # This function creates a message to be sent to the topic
    data = {
        'script_path': script_path,
        'requirements_path': requirements_path,
        'venv_name': venv_name,
        'execution_dir': execution_dir,
        'execution_id': str(execution_id)
    }
    return json.dumps(data)

def publish_message(connection: redis.Connection, topic, message):
    # This function publishes the message to the topic
    # You can replace this with your own custom logic
    connection.publish(topic, message)

def subscribe_to_topic(connection: redis.Connection, topic, handler):
    # This function connects to the topic
    # You can replace this with your own custom logic
    pubsub = connection.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(topic)
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield handler(message, message['data'])

    

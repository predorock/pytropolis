import redis
import rq
import json
import uuid
from lib.configuration.una_config import get_configuration


# get connection to redis
def get_connection():
    # This function initializes redis and the queue
    cfg = get_configuration()
    return redis.StrictRedis(host=cfg['redis_host'], port=cfg['redis_port'], db=cfg['redis_db'])

def get_connection_pool():
    # This function initializes redis with connection pool option
    cfg = get_configuration()
    connection_pool = redis.ConnectionPool(host=cfg['redis_host'], port=cfg['redis_port'], db=cfg['redis_db'])
    return connection_pool

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
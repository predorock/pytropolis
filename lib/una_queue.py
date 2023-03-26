from rq import Queue
from rq.job import Job
from redis import Redis
import json
import uuid

from .una_config import get_configuration

def queue_init(queue_name='una.py.runtime'):
    # This function initializes redis and the queue
    cfg = get_configuration()
    redis_conn = Redis(host=cfg['redis_host'], port=cfg['redis_port'], db=cfg['redis_db'])
    queue = Queue(queue_name, connection=redis_conn)

    return redis_conn, queue

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

def subscribe_to_topic(connection, topic, handler):
    # This function connects to the topic
    # You can replace this with your own custom logic
    pubsub = connection.pubsub()
    pubsub.subscribe(topic)
    for message in pubsub.listen():
        if message['type'] == 'message':
            handler(message['channel'], message['data'])

    

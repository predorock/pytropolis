import redis
import uuid
from rq import Queue, Connection

from lib.runner import handle_script_execution
from lib.configuration.una_config import get_configuration


def create_runner_task_payload(script_path, requirements_path, venv_name, execution_dir, execution_id=uuid.uuid4()):
    return {
        'script_path': script_path,
        'requirements_path': requirements_path,
        'venv_name': venv_name,
        'execution_dir': execution_dir,
        'execution_id': str(execution_id)
    }

def enqueue_runner_task(data):
    """
    Enqueue a task.
    :param task: The task to enqueue.
    :param config: The configuration for the task.
    :return: The task ID.
    """
    cfg = get_configuration()
    task = None
    with Connection(redis.from_url(cfg['redis_url'])) as conn:
            q = Queue(name=cfg['execution_queue'], connection=conn)
            task = q.enqueue(python_env_runner_task, data)
    return task
    

def python_env_runner_task(config):
    
    handle_script_execution(
        config['script_path'],
        config['requirements_path'],
        config['venv_name'],
        config['execution_id'],
    )

    return True
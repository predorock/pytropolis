import os

def get_configuration():
    home_dir = os.environ.get('PYT_HOME_DIR', os.path.join(os.getcwd(), 'volumes', 'pytropolis'))
    execution_dir = os.environ.get('PYT_EXECUTION_DIR', os.path.join(os.getcwd(), home_dir, 'executions'))
    log_dir = os.environ.get('PYT_LOG_DIR', os.path.join(os.getcwd(), home_dir, 'logs'))
    venv_container = os.environ.get('PYT_VENV_CONTAINER', os.path.join(os.getcwd(), home_dir, 'venv_container'))
    venv_default = os.path.join(venv_container, 'default')
    redis_host = os.environ.get('PYT_REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('PYT_REDIS_PORT', '6379'))
    redis_db = int(os.environ.get('PYT_REDIS_DB', '0'))
    redis_url = 'redis://{}:{}/{}'.format(redis_host, redis_port, redis_db)
    #topics
    execution_topict = os.environ.get('PYT_EXECUTION_TOPICT', 'pytropolis.execution')
    # queue name
    execution_queue = os.environ.get('PYT_EXECUTION_QUEUE', 'pytropolis.execution_queue')
    
    return {
        'home_dir': home_dir,
        'execution_dir': execution_dir,
        'log_dir': log_dir,
        'venv_container': venv_container,
        'venv_default': venv_default,
        'redis_host': redis_host,
        'redis_port': redis_port,
        'redis_db': redis_db,
        'redis_url': redis_url,
        'execution_topic': execution_topict,
        'execution_queue': execution_queue
    }

def configuration_setup():
    cfg = get_configuration()
    
    dir_check = [
        #home_dir must go first
        cfg['home_dir'],
        cfg['execution_dir'],
        cfg['log_dir']
    ]

    for d in dir_check:
        if not os.path.exists(d):
            os.mkdir(d)

    return cfg


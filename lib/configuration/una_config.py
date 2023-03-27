import os

def get_configuration():
    home_dir = os.environ.get('HOME_DIR', os.path.join(os.getcwd(), 'una-py-runtime'))
    execution_dir = os.environ.get('EXECUTION_DIR', os.path.join(os.getcwd(), home_dir, 'executions'))
    log_dir = os.environ.get('LOG_DIR', os.path.join(os.getcwd(), home_dir, 'logs'))
    venv_container = os.environ.get('VENV_CONTAINER', os.path.join(os.getcwd(), home_dir, 'una_venv_container'))
    venv_default = os.path.join(venv_container, 'default')
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', '6379'))
    redis_db = int(os.environ.get('REDIS_DB', '0'))
    redis_url = 'redis://{}:{}/{}'.format(redis_host, redis_port, redis_db)
    #topics
    topic_execution = os.environ.get('TOPIC_EXECUTION', 'una.py.runtime')
    
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
        'topic_execution': topic_execution
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


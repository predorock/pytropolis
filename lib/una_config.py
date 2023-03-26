import os

from .una_runner import create_or_get_virtualenv_path

def get_configuration():
    home_dir = os.environ.get('HOME_DIR', os.path.join(os.getcwd(), 'una-py-runtime'))
    execution_dir = os.environ.get('EXECUTION_DIR', os.path.join(os.getcwd(), home_dir, 'executions'))
    log_dir = os.environ.get('LOG_DIR', os.path.join(os.getcwd(), home_dir, 'logs'))
    venv_container = os.environ.get('VENV_CONTAINER', os.path.join(os.getcwd(), home_dir, 'una_venv_container'))
    venv_default = os.path.join(venv_container, 'default')
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', '6379'))
    redis_db = int(os.environ.get('REDIS_DB', '0'))
    
    return {
        'home_dir': home_dir,
        'execution_dir': execution_dir,
        'log_dir': log_dir,
        'venv_container': venv_container,
        'venv_default': venv_default,
        'redis_host': redis_host,
        'redis_port': redis_port,
        'redis_db': redis_db
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

    if not os.path.exists(cfg['venv_default']):
        create_or_get_virtualenv_path(cfg['venv_container'], 'default')


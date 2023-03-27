
from lib.runner import handle_script_execution

def python_env_runner_task(config):
    
    handle_script_execution(
        config['script_path'],
        config['requirements_path'],
        config['venv_name'],
        config['execution_id'],
    )

    return True
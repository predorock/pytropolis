import os
import uuid
import flask

from lib.configuration.una_config import get_configuration

def parse_request(request: flask.Request):
    """
    Parses the request and returns the script file path, requirements file path, and virtual environment name.
    """
    script_file = request.files['script']
    requirements_file = request.files['requirements']

    # check if the files are not null
    if not script_file:
        return flask.jsonify({'output_log': None, 'venv_name': venv_name, 'result': 'error', 'message': 'Script file is null.'})

    if not requirements_file:
        return flask.jsonify({'output_log': None, 'venv_name': venv_name, 'result': 'error', 'message': 'Requirements file is null.'})

    cfg = get_configuration()

    # retrieve optional configurations
    try:
        venv_name = request.form.get('venv_name')
    except KeyError:
        venv_name = 'default'
    
    try:
        script_name = request.form.get('script_name')
    except KeyError:
        script_name = 'algo'
    
    # create an exectution directory with uuid
    execution_id = str(uuid.uuid4())
    execution_dir = os.path.join(cfg['execution_dir'],f'{script_name}_{execution_id}')
    
    # make the execution directory if not exists recursively
    if not os.path.exists(execution_dir):
        os.makedirs(execution_dir)

    # Save files to disk
    script_path = os.path.join(execution_dir, f'{script_name}.py')
    script_file.save(script_path)

    requirements_path = os.path.join(execution_dir, f'{script_name}_requirements.txt')
    requirements_file.save(requirements_path)

    return script_path, requirements_path, venv_name, execution_dir, execution_id
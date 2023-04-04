import os
import uuid
import flask
import json

from pytropolis.configuration import get_configuration

def parse_request(request: flask.Request):
    """
    Parses the request and returns the script file path, requirements file path, and virtual environment name.
    """
    script_file = request.files['script']
    requirements_file = request.files['requirements']

    # check if the files are not null
    if not script_file:
        return flask.jsonify({'output_log': None, 'venv_name': None, 'result': 'error', 'message': 'Script file is null.'})

    if not requirements_file:
        return flask.jsonify({'output_log': None, 'venv_name': None, 'result': 'error', 'message': 'Requirements file is null.'})

    cfg = get_configuration()

    # retrieve optional configurations
    venv_name = request.form.get('venv_name', 'default')
    script_name = request.form.get('script_name', 'algo')
    script_argv = request.form.get('script_argv', None)
    env_vars = request.form.get('env_vars', None)

    if script_argv:
        script_argv = json.loads(script_argv)
    if env_vars:
        env_vars = json.loads(env_vars)
   
    # create an exectution directory with uuid
    execution_id = str(uuid.uuid4())
    execution_dir = os.path.join(cfg['execution_dir'],f'{script_name}_{execution_id}')
    
    # make the execution directory if not exists recursively
    if not os.path.exists(execution_dir):
        os.makedirs(execution_dir)

    # Save files to disk
    script_path = os.path.join(execution_dir, f'{script_name}.py')
    script_file.save(script_path)

    # Save requirements file to disk
    requirements_path = os.path.join(execution_dir, f'{script_name}_requirements.txt')
    requirements_file.save(requirements_path)
    
    return {
            "script_path": script_path, 
            "requirements_path": requirements_path, 
            "venv_name": venv_name, 
            "execution_dir": execution_dir, 
            "execution_id": execution_id,
            "env_vars": env_vars,
            "script_argv": script_argv
    }
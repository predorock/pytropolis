import os
import uuid
import subprocess
from flask import Flask, jsonify, request

from lib.una_config import get_configuration, configuration_setup
from lib.una_runner import create_or_get_virtualenv_path, install_dependencies, run_python_script, get_log_file_name
from lib.una_queue import queue_init, create_message, subscribe_to_topic

app = Flask(__name__)

def handle_script_execution(script_path, requirements_path, venv_name, execution_id=uuid.uuid4()):
    
    # extract configurations
    cfg = get_configuration()
    venv_container = cfg['venv_container']
    log_dir = cfg['log_dir']

    # Create or activate virtual environment
    venv_path = create_or_get_virtualenv_path(venv_container, venv_name)
    
    # Install dependencies
    try:
        install_dependencies(requirements_path, venv_path)
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': None, 'venv_name': venv_name, 'result': 'error', 'message': 'Error installing dependencies.'})
    
    # get the file name of the script
    script_name = os.path.basename(script_path)

    # Execute script
    log_file = os.path.join(log_dir, get_log_file_name(script_name, execution_id))
    try:
        run_python_script(script_path, log_file, venv_path)
        return jsonify({'output_log': log_file, 'venv_name': venv_name, 'result': 'success', 'message': 'Script executed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': log_file, 'venv_name': venv_name, 'result': 'error', 'message': 'Error executing script.'})

def parse_request(request):
    """
    Parses the request and returns the script file path, requirements file path, and virtual environment name.
    """
    script_file = request.files['script']
    requirements_file = request.files['requirements']

    # check if the files are not null
    if not script_file:
        return None, None, None, None, None
    
    if not requirements_file:
        return None, None, None, None, None

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

    requirements_path = os.path.join(execution_dir, 'requirements.txt')
    requirements_file.save(requirements_path)

    return script_path, requirements_path, venv_name, execution_dir, execution_id

# health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return 'OK'

@app.route('/run', methods=['POST'])
def run_script():
    # parse the request
    script_path, requirements_path, venv_name, execution_dir, execution_id = parse_request(request)
    
    # check if the files are not null
    if script_path is None:
        return jsonify({'output_log': None, 'venv_name': venv_name, 'result': 'error', 'message': 'Script file is null.'})
    if requirements_path is None:
        return jsonify({'output_log': None, 'venv_name': venv_name, 'result': 'error', 'message': 'Requirements file is null.'})
    
    # run the script
    return handle_script_execution(script_path, requirements_path, venv_name, execution_id)

@app.route('/enqueue', methods=['POST'])
def enqueue_execution():
    # parse the request
    script_path, requirements_path, venv_name = parse_request(request)
    # enqueue the script
    return handle_script_execution(script_path, requirements_path, venv_name)

if __name__ == '__main__':
    configuration_setup()
    #queue_init()
    app.run()

import subprocess
import os
import uuid
from flask import jsonify
from pytropolis.configuration import get_configuration
from pytropolis.runner.venv import install_dependencies, run_python_script, create_or_get_virtualenv_path, get_log_file_name


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

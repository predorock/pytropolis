import subprocess
import logging
import os
import uuid
from flask import jsonify
from pytropolis.configuration import get_configuration
from pytropolis.runner.venv import install_dependencies, create_or_get_virtualenv_path, get_log_file_name
import pytropolis.runner.parameters as pyt_params


def handle_script_execution(script_path, requirements_path, venv_name, execution_id=uuid.uuid4(), env_vars=None, script_argv=None):
    
    # extract configurations
    cfg = get_configuration()
    venv_container = cfg['venv_container']
    log_dir = cfg['log_dir']

    # Create or activate virtual environment
    venv_path = create_or_get_virtualenv_path(venv_container, venv_name, False)
    
    # Install dependencies
    try:
        install_dependencies(requirements_path, venv_path)
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': None, 'venv_name': venv_name, 'result': 'error', 'message': 'Error installing dependencies.'})
    
    # get the file name of the script
    script_name = os.path.basename(script_path)
    # Execute script
    log_file_path = os.path.join(log_dir, get_log_file_name(script_name, execution_id))
    # Create the command to execute the script
    
    python_path = os.path.join(venv_path, 'bin', 'python') if venv_path else 'python'
    
    # checking if the env vars are defined
    if env_vars:
        env_vars = pyt_params.params_to_env(env_vars)
    # checking if the script arguments are defined
    script_argv_list = pyt_params.params_to_args(script_argv) if script_argv else []
        
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Running script {script_path}\n with {python_path}...")
        logging.info(f"env: {env_vars}")
        
        process = subprocess.Popen([python_path, script_path] + script_argv_list, env=env_vars, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # Read the output of the process
        output, _ = process.communicate()
        # Write the output to the log file
        with open(log_file_path, 'w') as f:
            f.write(output.decode())


        return jsonify({'output_log': log_file_path, 'venv_name': venv_name, 'result': 'success', 'message': 'Script executed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': log_file_path, 'venv_name': venv_name, 'result': 'error', 'message': 'Error executing script.'})
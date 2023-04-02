import subprocess
import logging
import os
import uuid
from flask import jsonify
from pytropolis.configuration import get_configuration
from pytropolis.runner.venv import install_dependencies, create_or_get_virtualenv_path, get_log_file_name
from pytropolis.runner.parameters import env_vars_cmd


def create_script_command(venv_path, script_path, script_args=None, script_kwargs=None, env_params=None):
    """
    Returns the command to execute the specified script.
    """
    python_path = os.path.join(venv_path, 'bin', 'python') if venv_path else 'python'
    # TODO: add support for script arguments
    python_command = f'{script_path}'
    if env_params:
        env_vars = env_vars_cmd(env_params)
        python_command = f'{env_vars} {python_command}'
    return python_path, python_command
   


def handle_script_execution(script_path, requirements_path, venv_name, execution_id=uuid.uuid4(), env_params=None):
    
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
    log_file = os.path.join(log_dir, get_log_file_name(script_name, execution_id))
    # Create the command to execute the script
    python_path, python_command = create_script_command(venv_path, script_path, env_params=env_params)
    try:
        run_python_script(python_path, python_command, log_file)
        return jsonify({'output_log': log_file, 'venv_name': venv_name, 'result': 'success', 'message': 'Script executed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': log_file, 'venv_name': venv_name, 'result': 'error', 'message': 'Error executing script.'})

def run_python_script(python_bin_path, python_script_command, log_file_path):
    """
    Runs the specified Python script using the Python interpreter in the fixed virtual environment,
    and redirects the logs to a file.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Running script {python_script_command}\n with {python_bin_path}...")
    
    if not os.path.exists(python_bin_path):
        raise FileNotFoundError(f"Python interpreter not found at {python_bin_path}")
    if not os.path.exists(python_script_command):
        raise FileNotFoundError(f"Python script not found at {python_script_command}")
    
    # Open the process with the subprocess.PIPE stdout
    process = subprocess.Popen([python_bin_path, python_script_command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Read the output of the process
    output, _ = process.communicate()
    # Write the output to the log file
    with open(log_file_path, 'w') as f:
        f.write(output.decode())

    return output
import os
import subprocess
import logging
import uuid

def activate_virtualenv(venv_path):
    """
    Activates the virtual environment at the specified path.
    """
    activate_venv_cmd = 'source ' + os.path.join(venv_path, 'bin', 'activate')
    subprocess.check_output(activate_venv_cmd, shell=True)

def create_or_get_virtualenv_path(venv_container, venv_name, activate=True):
    """
    If a virtual environment already exists at the specified path, activates it. If not, creates a new virtual environment
    at the specified path.
    """
    
    venv_path = os.path.join(venv_container, venv_name) if venv_name else 'default'

    if venv_path:
        if not os.path.exists(os.path.join(venv_path, 'bin', 'python')):
            create_venv_cmd = f'python3 -m venv {venv_path}'
            subprocess.check_output(create_venv_cmd, shell=True)
    else:
        raise FileNotFoundError("Virual environment path is not valid.")
    
    if activate:
        activate_virtualenv(venv_path)
    
    return venv_path


def install_dependencies(requirements_path, venv_path):
    """
    Installs any dependencies listed in the given requirements file.
    """
    pip_path = os.path.join(venv_path, 'bin', 'pip') if venv_path else 'pip'
    subprocess.check_output([pip_path, 'install', '-r', requirements_path])


def run_python_script(script_path, log_file_path, venv_path):
    """
    Runs the specified Python script using the Python interpreter in the fixed virtual environment,
    and redirects the logs to a file.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Running script {script_path} in virtual environment {venv_path}...")

    # Open the process with the subprocess.PIPE stdout
    process = subprocess.Popen([os.path.join(venv_path, 'bin', 'python'), script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Read the output of the process
    output, _ = process.communicate()
    # Write the output to the log file
    with open(log_file_path, 'w') as f:
        f.write(output.decode())

    return output

def get_log_file_name(script_name, execution_id=uuid.uuid4()):
    """
    Returns a unique log file name with the specified script name as prefix.
    """
    return f"{script_name.split('.')[0]}_{str(execution_id)}.log"


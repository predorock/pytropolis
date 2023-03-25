import os
import subprocess
import logging
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)

log_dir = os.environ.get('LOG_DIR', os.path.join(os.getcwd(), 'logs'))
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

venv_path = os.path.join(os.getcwd(), 'venv')


@app.route('/runscript', methods=['POST'])
def run_script():
    """
    Receives a Python script and requirements file from the request, installs any dependencies listed in the requirements
    file in the fixed virtual environment, runs the script with the given file path in the fixed virtual environment,
    and logs the output to a file. The path to the log file and the result of running the script are returned as a JSON response.
    """
    script_file = request.files['script']
    requirements_file = request.files['requirements']

    # Save files to disk
    script_path = os.path.join(os.getcwd(), 'received_script.py')
    requirements_path = os.path.join(os.getcwd(), 'received_requirements.txt')
    script_file.save(script_path)
    requirements_file.save(requirements_path)

    # Install dependencies
    try:
        install_dependencies(requirements_path)
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': None, 'result': 'error'})

    # Execute script
    log_file = os.path.join(log_dir, get_log_file_name(script_file.filename))
    try:
        run_python_script(script_path, log_file)
        return jsonify({'output_log': log_file, 'result': 'success'})
    except subprocess.CalledProcessError as e:
        return jsonify({'output_log': log_file, 'result': 'error'})


def install_dependencies(requirements_path):
    """
    Installs any dependencies listed in the given requirements file.
    """
    subprocess.check_output([os.path.join(venv_path, 'bin', 'pip'), 'install', '-r', requirements_path])


def run_python_script(script_path, log_file):
    """
    Runs the specified Python script using the Python interpreter in the fixed virtual environment,
    and redirects the logs to a file.
    """
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logging.info(f"Executing script: {script_path}")

    # Open the process with the subprocess.PIPE stdout
    process = subprocess.Popen([os.path.join(venv_path, 'bin', 'python'), script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Read the output of the process
    output, _ = process.communicate()
    # Write the output to the log file
    with open(log_file, 'w') as f:
        f.write(output.decode())

    return output


def get_log_file_name(script_name):
    """
    Returns a unique log file name with the specified script name as prefix.
    """
    return f"{script_name.split('.')[0]}_{uuid.uuid4()}.log"


if __name__ == '__main__':
    app.run()

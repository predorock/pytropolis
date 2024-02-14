from flask import request, Blueprint, jsonify

from pytropolis.runner import handle_script_execution
from pytropolis.tasks.runner_task import enqueue_runner_task
from pytropolis.blueprints.runner_bp.common import parse_request

runner_bp = Blueprint('runner_bp', __name__, url_prefix='/api/runner')

@runner_bp.route('/start', methods=['POST'])
def run_script():
    """
    Execute a script
    ---
    tags:
      - Runner API
    consumes:
      - multipart/form-data
    parameters:
      - name: script
        in: formData
        type: file
        required: true
        description: The Python script to execute.
      - name: requirements
        in: formData
        type: file
        required: true
        description: The requirements file for the script.
      - name: venv_name
        in: formData
        type: string
        required: false
        default: default
        description: The name of the virtual environment to use.
      - name: script_name
        in: formData
        type: string
        required: false
        default: algo
        description: The name of the script.
      - name: env_params
        in: formData
        type: JSON
        required: false
        default: {}
        description: The environment parameters to use.
      - name: script_args
        in: formData
        type: JSON
        required: false
        default: {}
        description: The arguments to pass to the script.
    responses:
      200:
        description: Success
        schema:
          id: execution_result
          properties:
            output_log:
              type: string
              description: The path to the log file containing the script's output.
            venv_name:
              type: string
              description: The name of the virtual environment used.
            result:
              type: string
              description: The result of the script execution ('success' or 'error').
            message:
              type: string
              description: A message describing the result of the script execution.
      400:
        description: Bad Request
    """
    # parse the request
    request_params = parse_request(request)    
    # run the script
    return handle_script_execution(request_params['script_path'], request_params['requirements_path'], request_params['venv_name'], request_params['execution_id'], env_vars=request_params['env_vars'], script_argv=request_params['script_argv'])

@runner_bp.route('/enqueue', methods=['POST'])
def enqueue_execution():
    """
    Enqueue a script
    ---
    tags:
      - Runner API
    consumes:
      - multipart/form-data
    parameters:
      - name: script
        in: formData
        type: file
        required: true
        description: The Python script to execute.
      - name: requirements
        in: formData
        type: file
        required: true
        description: The requirements file for the script.
      - name: venv_name
        in: formData
        type: string
        required: false
        default: default
        description: The name of the virtual environment to use.
      - name: script_name
        in: formData
        type: string
        required: false
        default: algo
        description: The name of the script.
      - name: env_params
        in: formData
        type: JSON
        required: false
        default: {}
        description: The environment parameters to use.
      - name: script_args
        in: formData
        type: JSON
        required: false
        default: {}
        description: The arguments to pass to the script.
    responses:
      200:
        description: Success
        schema:
          id: execution_result
          properties:
            output_log:
              type: string
              description: The path to the log file containing the script's output.
            venv_name:
              type: string
              description: The name of the virtual environment used.
            result:
              type: string
              description: The result of the script execution ('success' or 'error').
            message:
              type: string
              description: A message describing the result of the script execution.
      400:
        description: Bad Request
    """
    # parse the request
    request_params = parse_request(request)    
    # enqueue the job
    task = enqueue_runner_task(request_params)
    return jsonify({'job': task.get_id(), 'result': 'success', 'message': 'Script enqueued.', 'data': request_params})
from flask import Blueprint, jsonify, request

from pytropolis.blueprints.common import parse_request
from pytropolis.tasks.runner_task import create_runner_task_payload, enqueue_runner_task

queue_bp = Blueprint('queue_bp', __name__)

@queue_bp.route('/api/enqueue', methods=['POST'])
def enqueue_execution():
    """
    Enqueue a script
    ---
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
    script_path, requirements_path, venv_name, execution_dir, execution_id = parse_request(request) 
    # create the payload
    data = create_runner_task_payload(script_path, requirements_path, venv_name, execution_dir, execution_id)
    # enqueue the job
    task = enqueue_runner_task(data)
    
    return jsonify({'job': task.get_id(), 'result': 'success', 'message': 'Script enqueued.', 'data': data})
from flask import request, Blueprint

from pytropolis.blueprints.common import parse_request
from pytropolis.runner import handle_script_execution

runner_bp = Blueprint('runner_bp', __name__)

@runner_bp.route('/api/run', methods=['POST'])
def run_script():
    """
    Execute a script
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
    # run the script
    return handle_script_execution(script_path, requirements_path, venv_name, execution_id)
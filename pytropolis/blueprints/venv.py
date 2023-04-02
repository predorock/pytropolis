import os
from flask import Blueprint, jsonify, request
from pytropolis.configuration import get_configuration
from pytropolis.runner.venv import create_or_get_virtualenv_path, install_dependencies, get_installed_libraries

venv_bp = Blueprint('venv_bp', __name__)
# returns the list of virtual environments
@venv_bp.route('/api/venv', methods=['GET'])
def get_venv_list():
    """
    Get the list of virtual environments
    ---
    tags:
      - Virtual Environment API
    responses:
      200:
        description: Success
        schema:
          id: venv_list
          properties:
            venv_list:
              type: array
              items:
                type: string
                description: The name of a virtual environment.
    """
    # get the venv container path
    venv_container_path = get_configuration()['venv_container']
    # get the list of virtual environments
    venv_list = [venv for venv in os.listdir(venv_container_path) if os.path.isdir(os.path.join(venv_container_path, venv))]
    # get the installed packages for each virtual environment
    data = {}
    
    for venv in venv_list:
        data[venv] = get_installed_libraries(os.path.join(venv_container_path, venv))

    # return the list of virtual environments
    return jsonify({'venv_list': data})


# creates a new virtual environment
@venv_bp.route('/api/venv', methods=['POST'])
def create_venv():
    """
    Create a new virtual environment
    ---
    tags:
      - Virtual Environment API
    consumes:
      - multipart/form-data
    parameters:
      - name: venv_name
        in: formData
        type: string
        required: true
        description: The name of the virtual environment to create.
      - name: requirements_file
        in: formData
        type: file
        required: false
        description: The requirements file for the virtual environment.
    responses:
      200:
        description: Success
        schema:
          id: venv_creation_result
          properties:
            message:
              type: string
              description: A message describing the result of the virtual environment creation.
            venv_path:
              type: string
              description: The path to the virtual environment.
      400:
        description: Bad Request
    """
    # get virtual environment name
    venv_name = request.form['venv_name']
    # get the venv container path
    venv_container_path = get_configuration()['venv_container']
    # if the venv already exists return an error
    if os.path.isdir(os.path.join(venv_container_path, venv_name)):
        return jsonify({'message': f'Virtual environment {venv_name} already exists.'}), 400
    # create the virtual environment
    venv_path = create_or_get_virtualenv_path(venv_container_path, venv_name, False)

    return jsonify({'message': f'Virtual environment {venv_name} created.', 'venv_path': venv_path}), 200


# updata a virtual environment with a requirements file
@venv_bp.route('/api/venv', methods=['PUT'])
def update_venv():
    """
    Update a virtual environment with a requirements file
    ---
    tags:
      - Virtual Environment API
    consumes:
      - multipart/form-data
    parameters:
      - name: venv_name
        in: formData
        type: string
        required: true
        description: The name of the virtual environment to create.
      - name: requirements_file
        in: formData
        type: file
        required: false
        description: The requirements file for the virtual environment.
    responses:
      200:
        description: Success
        schema:
          id: venv_creation_result
          properties:
            message:
              type: string
              description: A message describing the result of the virtual environment creation.
            venv_path:
              type: string
              description: The path to the virtual environment.
      400:
        description: Bad Request
    """
    # get virtual environment name
    venv_name = request.form['venv_name']
    # get the requirements file
    requirements_file = request.files['requirements_file']
    # get the venv container path
    venv_container_path = get_configuration()['venv_container']
    # if the venv already exists return an error
    if not os.path.isdir(os.path.join(venv_container_path, venv_name)):
        return jsonify({'message': f'Virtual environment {venv_name} does not exist.'}), 400
    # create the virtual environment
    venv_path = create_or_get_virtualenv_path(venv_container_path, venv_name, True)
    # install the requirements
    install_dependencies(venv_path, requirements_file)

    return jsonify({'message': f'Virtual environment {venv_name} updated.', 'venv_path': venv_path}), 200

# deletes a virtual environment
@venv_bp.route('/api/venv', methods=['DELETE'])
def delete_venv():
    """
    Delete a virtual environment
    ---
    tags:
      - Virtual Environment API
    consumes:
      - multipart/form-data
    parameters:
      - name: venv_name
        in: formData
        type: string
        required: true
        description: The name of the virtual environment to delete.
    responses:
      200:
        description: Success
        schema:
          id: venv_deletion_result
          properties:
            message:
              type: string
              description: A message describing the result of the virtual environment deletion.
    """
    # get virtual environment name
    venv_name = request.form['venv_name']
    # get the venv container path
    venv_container_path = get_configuration()['venv_container']

    # if the name of the environment is 'default' return an error
    if venv_name == 'default':
        return jsonify({'message': f'Virtual environment {venv_name} cannot be deleted.'}), 400
    
    # if the venv does not exist return an error
    if not os.path.isdir(os.path.join(venv_container_path, venv_name)):
        return jsonify({'message': f'Virtual environment {venv_name} does not exist.'}), 400
    # delete the virtual environment
    venv_path = os.path.join(venv_container_path, venv_name)
    os.system(f'rm -rf {venv_path}')

    return jsonify({'message': f'Virtual environment {venv_name} deleted.'}), 200
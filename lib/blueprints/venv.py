import os
from flask import Blueprint, jsonify
from lib.configuration.una_config import get_configuration


venv_bp = Blueprint('venv_bp', __name__)
# returns the list of virtual environments
@venv_bp.route('/api/venv', methods=['GET'])
def get_venv_list():
    """
    Get the list of virtual environments
    ---
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
        venv_path = os.path.join(venv_container_path, venv)
        # get the list of installed packages
        venv_packages = [package for package in os.listdir(os.path.join(venv_path, 'lib', 'python3.8', 'site-packages')) if os.path.isdir(os.path.join(venv_path, 'lib', 'python3.8', 'site-packages', package))]
        # add the list of installed packages to the virtual environment
        data[venv] = venv_packages
    # return the list of virtual environments
    return jsonify({'venv_list': data})
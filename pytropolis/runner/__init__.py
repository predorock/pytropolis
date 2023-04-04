import subprocess
import logging
import os
import uuid
from flask import jsonify
from pytropolis.configuration import get_configuration
from pytropolis.runner.venv import install_dependencies, create_or_get_virtualenv_path, get_log_file_name
import pytropolis.runner.parameters as pyt_params


class ScriptParamsException(Exception):
    pass

# class that defines the params of the script
class ScriptExectionParams:
    def __init__(self, script_path, requirements_path, venv_name, execution_id, env_params=None, script_params=None):
        self.script_path = script_path
        self.requirements_path = requirements_path
        self.venv_name = venv_name
        self.execution_id = execution_id
        self.env_params = env_params
        self.script_params = script_params
        self.__check__()
        self.__venv_path__ = create_or_get_virtualenv_path(self.venv_name)
        self.__venv_py_path__ = os.path.join(self.__venv_path__, 'bin', 'python') if self.venv_name else 'python'

    def __check__(self):
        """
        Checks if the params are valid.
        """
        if not self.script_path:
            raise ScriptParamsException('Script path is not defined.')
        if not self.requirements_path:
            raise ScriptParamsException('Requirements path is not defined.')
        if not self.venv_name:
            raise ScriptParamsException('Virtual environment name is not defined.')
        if not self.execution_id:
            raise ScriptParamsException('Execution id is not defined.')
        return None
    
    # returns the json representation of the object
    def json(self):
        """
        Returns the json representation of the object.
        """
        return {
            "script_path": self.script_path,
            "requirements_path": self.requirements_path, 
            "venv_name": self.venv_name, 
            "execution_id": self.execution_id,
            "env_params": self.env_params,
            "script_params": self.script_params
        }
    
    # creates the script execution params from the request
    def create_script_command(self):
        """
        Returns the command to execute the specified script.
        """
        python_command = f'{self.script_path}'
        if self.env_params:
            env_vars = self.sanitize_args(self.env_vars_cmd())
            python_command = f'{env_vars} {python_command}'
        if self.script_params:
            script_args = self.sanitize_args(self.args_cmd())
            python_command = f'{python_command} {script_args}'

        return self.__venv_py_path__, python_command
    
    def params_to_env(self):
        return pyt_params.params_to_env(self.env_params)
    
    def env_vars_cmd(self):
        return pyt_params.env_vars_cmd(self.env_params)
    
    def params_to_args(self):
        return pyt_params.params_to_args(self.script_params)
    
    def args_cmd(self):
        return pyt_params.args_cmd(self.script_params)
    
    def sanitize_args(self, cmd):
        return pyt_params.sanitize_args(cmd)


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

def params_to_env(params):
    """Converts a dictionary of parameters to a dictionary of environment variables."""
    env = {}
    for k, v in params.items():
        env[k.upper()] = str(v)
    return env

def env_vars_cmd(params):
    """Returns a string of environment variables to be used in a subprocess call."""
    env = params_to_env(params)
    return ' '.join([f'{k}={v}' for k, v in env.items()])
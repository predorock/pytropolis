import re

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

def params_to_args(params):
    """Converts a dictionary of parameters to a list of arguments."""
    args = []
    for k, v in params.items():
        args.append(f'--{k}')
        args.append(str(v))
    return args

def args_cmd(params):
    """Returns a string of arguments to be used in a subprocess call."""
    args = params_to_args(params)
    return ' '.join(args)    

def sanitize_args(args):
    """Sanitizes a list of command-line arguments to prevent script injection."""
    sanitized_args = []
    pattern = re.compile(r'[^\w\s\-.,:;/]')
    for arg in args:
        sanitized_arg = pattern.sub('', arg)
        sanitized_args.append(sanitized_arg)
    return args

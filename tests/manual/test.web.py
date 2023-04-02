import json
import requests

url = 'http://localhost:5000/api/runner/start'

# Set up the files to send with the request
script_file = open('../resources/hello/ascii_title.py', 'rb')
requirements_file = open('../resources/hello/requirements.txt', 'rb')

data = {
    'script_name': 'ascii_title',
    'venv_name': 'ascii_title',
    'env_params': json.dumps({'ART_title': 'PHEEGA!'}),
}

files = {'script': script_file, 'requirements': requirements_file}

# Send the request and get the response
response = requests.post(url, data=data, files=files)

if response.ok:
    result = response.json()
    print(f"Script execution result:\n{json.dumps(result, indent=2)}")
else:
    error = response.reason
    print(f"Error executing script:\n{error}")

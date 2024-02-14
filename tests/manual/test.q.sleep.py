import json
import requests
import sys

# Get the number from program arguments
req_number = 1
if len(sys.argv) > 1:
    req_number = int(sys.argv[1])

url = 'http://localhost:5000/api/runner/enqueue'

# Set up the files to send with the request
script_file = open('../resources/hello/sleep.py', 'rb')
requirements_file = open('../resources/hello/requirements.txt', 'rb')

data = {
    'script_name': 'sleep',
    'venv_name': 'sleep'
}

files = {'script': script_file, 'requirements': requirements_file}

# Send the request and get the response
for i in range(req_number):
    response = requests.post(url, data=data, files=files)
    if response.ok:
        result = response.json()
        print(f"Script execution result:\n{json.dumps(result, indent=2)}")
    else:
        error = response.reason
        print(f"Error executing script:\n{error}")

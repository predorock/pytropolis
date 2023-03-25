import os
import requests

url = 'http://localhost:5000/runscript'

# Set up the files to send with the request
script_file = open('../resources/hello/ascii_title.py', 'rb')
requirements_file = open('../resources/hello/requirements.txt', 'rb')

# Send the request and get the response
response = requests.post(url, files={'script': script_file, 'requirements': requirements_file})

# Close the file objects
script_file.close()
requirements_file.close()

# Check for errors and print the result
if response.ok:
    result = response.json()
    print(f"Script execution result:\n{result}")
else:
    error = response.json()
    print(f"Error executing script:\n{error}")

import os
import unittest
import tempfile
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_run_script(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            script_file_path = os.path.join(temp_dir, 'test_script.py')
            with open(script_file_path, 'w') as f:
                f.write('print("Hello World!")')

            requirements_file_path = os.path.join(temp_dir, 'test_requirements.txt')
            with open(requirements_file_path, 'w') as f:
                f.write('flask\n')

            # Make POST request to run script
            with app.test_request_context('/runscript', method='POST', data={
                'script': open(script_file_path, 'rb'),
                'requirements': open(requirements_file_path, 'rb')
            }):
                response = app.full_dispatch_request()

            # Check response
            self.assertEqual(response.status_code, 200)
            self.assertIn('result', response.json)
            self.assertEqual(response.json['result'], 'Hello World!\n')

            # Check log file
            log_file_path = os.path.join(temp_dir, 'test_script.log')
            self.assertTrue(os.path.isfile(log_file_path))
            with open(log_file_path, 'r') as f:
                self.assertIn('Executing script', f.read())

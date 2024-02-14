from flask import Blueprint, send_from_directory, redirect

import os

core = Blueprint('core',__name__)

@core.route('/')
def hello():
    return redirect("/api/docs", code=302)

# health check endpoint
@core.route('/health', methods=['GET'])
def health():
    """
    Health Check
    ---
    responses:
      200:
        description: OK
    """
    return 'OK'


@core.route('/files/<path:path>', methods=['GET'])
def send_report(path):
    """
    Download a file from a given path
    ---
    responses:
      200:
        description: OK
    """
    s_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(s_folder, path)
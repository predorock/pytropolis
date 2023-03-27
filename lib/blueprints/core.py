from flask import Blueprint, send_from_directory, redirect
core = Blueprint('core', __name__,)

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


@core.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)
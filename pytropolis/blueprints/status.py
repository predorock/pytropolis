
from flask import Blueprint, Response

status_bp = Blueprint('status_bp', __name__)

@status_bp.route('/api/status')
def stream():
    """
    Get the status of the execution workers
    ---
    responses:
      200:
        description: OK
    """
    return Response("status", mimetype="text/json")
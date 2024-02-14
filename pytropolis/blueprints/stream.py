
from flask import Blueprint, Response
from pytropolis.broker import get_connection
from pytropolis.configuration import get_configuration

steam_bp = Blueprint('stream_bp', __name__)

def event_stream():
    topic  = get_configuration()['execution_topic']
    pubsub = get_connection().pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(topic)
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

@steam_bp.route('/api/stream')
def stream():
    """
    Event stream of the execution queue
    ---
    responses:
      200:
        description: OK
    """
    return Response(event_stream(), mimetype="text/event-stream")
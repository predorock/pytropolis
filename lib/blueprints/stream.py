
from flask import Blueprint, Response
from lib.una_broker import get_publisher, get_configuration

steam_bp = Blueprint('stream_bp', __name__,)

def event_stream():
    pubsub = get_publisher().pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(get_configuration()['topic_execution'])
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

@steam_bp.route('/api/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")
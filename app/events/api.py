import datetime
from app import application
from flask import jsonify, request
from app.sessions import session_manager
from app.auth.authentication import requires_auth



@application.route('/event/register', methods=['POST'])
@requires_auth
def register_event():
    json = request.get_json()
    print "received request " + str(json)
    user_id = json['user_id']
    event_type = json['event_type']
    session = session_manager.create_or_update_session(user_id, event_type)
    response = jsonify(
        session_id=5 #session.id,
    )
    return response

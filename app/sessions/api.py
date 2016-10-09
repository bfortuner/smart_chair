import datetime
from app import application
from flask import jsonify, request
from app.sessions import session_manager
from app.auth.authentication import requires_auth


@application.route('/event/register', methods=['POST'])
def register_event():
    json = request.get_json()
    print "Received request " + str(json)
    username = json['username']
    event_type = json['event_type']
    session = session_manager.create_or_update_session(username, event_type)
    print "Returning session: %s" % session
    response = jsonify(
        session_id=session.id,
        username=session.username,
        session_start_time=session.start_time,
        last_posture_event=session.last_posture_signal_time,
        last_sitting_event=session.last_sitting_signal_time
    )
    return response



@application.route('/sessions/<username>', methods=['GET'])
def get_sessions(username):
    sessions = session_manager.get_all_user_sessions(username)
    return jsonify(sessions=sessions)
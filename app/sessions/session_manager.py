from app import db
from sqlalchemy.sql import case, func
from app.sessions.models import Session
from app.events.constants import SITTING_EVENT, POSTURE_EVENT
import datetime


def get_current_time():
    return datetime.datetime.now()


def create_or_update_session(username, event_type):
    open_session = get_users_last_open_session(username)
    if open_session is None:
        print "Creating new session for username %s" % username
        return create_new_session(username)
    elif event_type == SITTING_EVENT:
        register_sitting_event(open_session.id)
    elif event_type == POSTURE_EVENT:
        register_posture_event(open_session.id)
    else:
        "Event type %s not found!" % event_type


def get_users_last_open_session(username):
    # query for the user's last open session
    return None


def create_new_session(username):
    print "Creating new session"
    # Create new user session
    session = Session(username)
    db.add(session)
    db.commit()
    return session


def register_sitting_event(session_id):
    # update session last_sitting_signal_time to get_current_time()
    pass


def register_posture_event(session_id):
    # update session last_posture_signal_time to get_current_time()
    pass


def close_session(session_id):
    # update session end_time to datetime.datetime.now()
    pass

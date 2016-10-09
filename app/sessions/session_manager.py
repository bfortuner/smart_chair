from app import db
from sqlalchemy.sql import case, func
from app.sessions.models import Session
from app.sessions.constants import MAX_STALE_SESSION_TIME_SECS
from app.events.constants import SITTING_EVENT, POSTURE_EVENT
import datetime


def get_current_time_utc():
    return datetime.datetime.utcnow()


def update_last_sitting_reminder_sent_time(session):
    print "Updating last sitting reminder sent to now"
    session.last_sitting_reminder_sent = get_current_time_utc()
    db.commit()


def update_last_posture_reminder_sent_time(session):
    print "Updating last posture reminder sent to now"
    session.last_posture_reminder_sent = get_current_time_utc()
    db.commit()


def create_or_update_session(username, event_type):
    open_session = get_users_current_session(username)
    if open_session is None:
        print "Creating new session for username %s" % username
        return create_new_session(username)

    print "Found existing session %s" % open_session
    if event_type.lower() == SITTING_EVENT:
        return register_sitting_event(open_session)
    elif event_type.lower() == POSTURE_EVENT:
        return register_posture_event(open_session)
    else:
        msg = "Event type %s not found!" % event_type
        raise Exception(msg)


def get_stale_sessions():
    # Return all sessions where user is no longer sitting
    earliest_non_stale_session_time = (get_current_time_utc()
            - datetime.timedelta(seconds=MAX_STALE_SESSION_TIME_SECS))
    sessions = (db.query(Session)
                .filter(Session.end_time == None)
                .filter(Session.last_sitting_signal_time < earliest_non_stale_session_time)
                .filter(Session.last_posture_signal_time < earliest_non_stale_session_time)
                .all())
    return sessions


def get_users_current_session(username):
    session = (db.query(Session)
                .filter_by(username=username)
                .filter(Session.end_time == None)
                .order_by(Session.last_sitting_signal_time.desc())
                .first())
    return session


def get_all_user_sessions(username):
    sessions = (db.query(Session)
                .with_entities(Session.id, Session.start_time, 
                    Session.last_sitting_signal_time, Session.last_posture_signal_time)
                .filter_by(username=username)
                .order_by(Session.last_sitting_signal_time.desc())
                .all())
    return sessions


def create_new_session(username):
    print "Creating new sitting session"
    session = Session(username)
    db.add(session)
    db.commit()
    return session


def register_sitting_event(session):
    session.last_sitting_signal_time = get_current_time_utc()
    db.commit()
    return session


def register_posture_event(session):
    session.last_posture_signal_time = get_current_time_utc()
    db.commit()
    return session


def close_session(session):
    session.end_time = get_current_time_utc()
    db.commit()

import datetime
from app.sessions import session_manager
from app.reminders.constants import MAX_ALLOWED_POSTURE_SIGNAL_GAP_SECS, MAX_SECONDS_OF_NON_INTERRUPTED_SITTING
from app.events.constants import SITTING_EVENT, POSTURE_EVENT


def get_current_time_utc():
    return datetime.datetime.utcnow()


def get_user_reminders(username):
    reminders = {SITTING_EVENT: False, POSTURE_EVENT: False}
    current_session = session_manager.get_users_current_session(username)
    if current_session is None:
        return reminders

    reminders[SITTING_EVENT] = get_sitting_reminder(current_session)
    reminders[POSTURE_EVENT] = get_posture_reminder(current_session)
    return reminders


def get_sitting_reminder(session):
	session_length = (get_current_time_utc() - session.start_time).total_seconds()
	return session_length > MAX_SECONDS_OF_NON_INTERRUPTED_SITTING


def get_posture_reminder(session):
    last_required_posture_time = (get_current_time_utc() - datetime.timedelta(seconds=MAX_ALLOWED_POSTURE_SIGNAL_GAP_SECS))
    return session.last_posture_signal_time < last_required_posture_time


def send_reminder(username):
    print "Sending reminder and closing session"
    session = session_manager.get_users_current_session(username)
    if session is not None:
    	session_manager.close_session(session)
    print "No open sessions for user: %s" % username

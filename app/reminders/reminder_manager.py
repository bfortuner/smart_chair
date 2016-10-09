import datetime
from app.sessions import session_manager
from app.reminders.constants import MAX_SECONDS_OF_NON_INTERRUPTED_SITTING
from app.reminders.constants import MAX_ALLOWED_SITTING_SIGNAL_GAP_SECS, MAX_ALLOWED_POSTURE_SIGNAL_GAP_SECS
from app.reminders.constants import MIN_INTERVAL_BETWEEN_REMINDERS
from app.events.constants import SITTING_EVENT, POSTURE_EVENT



def get_current_time_utc():
    return datetime.datetime.utcnow()


def get_user_reminders(username):
    reminders = {
        "send_sitting_reminder": False,
        "send_posture_reminder": False,
        "status": "No Open Session"
    }
    current_session = session_manager.get_users_current_session(username)
    if current_session is None:
        reminders["status"] = "No Open Sessions"
        print "No open sessions for username: %s" % username
        return reminders

    reminders["session_id"] = current_session.id
    reminders["last_recorded_sitting"] = current_session.last_sitting_signal_time
    reminders["last_recorded_posture"] = current_session.last_posture_signal_time
    reminders["session_start_time"] = current_session.start_time
    if current_session.last_sitting_reminder_sent is not None:
        reminders["last_sitting_reminder_sent"] = current_session.last_sitting_reminder_sent

    if should_skip_reminder_cycle(current_session):
        status_msg = ("Skipped Current Reminders b/c " +
                               "user has seen reminder too recently")
        print status_msg
        reminders["status"] = status_msg
        return reminders

    print "Calculating reminders"
    reminders["send_sitting_reminder"] = get_sitting_reminder(current_session)
    reminders["send_posture_reminder"] = get_posture_reminder(current_session)
    reminders["status"] = "Calculated Current Reminders"

    return reminders


def should_skip_reminder_cycle(session):
    print "Last sitting reminder sent: " + str(session.last_sitting_reminder_sent)
    if session.last_sitting_reminder_sent is None:
        print "No reminders have been sent"
        return False
    print "Calculating Reminder Skip Cycle Window"
    next_open_reminder_window = (
        session.last_sitting_reminder_sent 
        + datetime.timedelta(seconds=MIN_INTERVAL_BETWEEN_REMINDERS))
    should_skip = get_current_time_utc() < next_open_reminder_window
    print "Should skip: " + str(should_skip)
    return should_skip


def get_sitting_reminder(session):
    session_length = (get_current_time_utc() -
                      session.start_time).total_seconds()
    return session_length > MAX_SECONDS_OF_NON_INTERRUPTED_SITTING


def get_posture_reminder(session):
    last_required_posture_time = (get_current_time_utc(
    ) - datetime.timedelta(seconds=MAX_ALLOWED_POSTURE_SIGNAL_GAP_SECS))
    last_required_sitting_time = (get_current_time_utc(
    ) - datetime.timedelta(seconds=MAX_ALLOWED_SITTING_SIGNAL_GAP_SECS))
    posture_reminder_triggered = session.last_posture_signal_time < last_required_posture_time
    user_still_sitting = session.last_sitting_signal_time > last_required_sitting_time
    return posture_reminder_triggered and user_still_sitting


def send_reminder(username):
    print "Sending reminder and closing session"
    session = session_manager.get_users_current_session(username)
    if session is not None:
        status_msg = "Sending reminder and updating last reminder time"
        session_manager.update_last_sitting_reminder_sent_time(session)
    else:
        status_msg = "No open sessions for user: %s" % username
    return status_msg

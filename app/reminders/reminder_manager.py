import datetime
from app.sessions import session_manager
from app.reminders.constants import MAX_SECONDS_OF_NON_INTERRUPTED_SITTING
from app.reminders.constants import MAX_ALLOWED_SITTING_SIGNAL_GAP_SECS, MAX_ALLOWED_POSTURE_SIGNAL_GAP_SECS
from app.config import config
from app.events.constants import SITTING_EVENT, POSTURE_EVENT


def get_current_time_utc():
    return datetime.datetime.utcnow()


def get_user_reminders(username):
    reminders = {
        "send_sitting_reminder": False,
        "send_posture_reminder": False,
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
        reminders[
            "last_sitting_reminder_sent"] = current_session.last_sitting_reminder_sent
    if current_session.last_posture_reminder_sent is not None:
        reminders[
            "last_posture_reminder_sent"] = current_session.last_posture_reminder_sent

    reminders["sitting_too_long"] = get_sitting_reminder(current_session)
    reminders["posture_incorrect"] = get_posture_reminder(current_session)

    if should_skip_sitting_reminder_cycle(current_session):
        status_msg = ("Skipped Current Sitting Reminder b/c " +
                      "user has seen sitting reminder too recently")
        reminders["status"] = status_msg
        reminders["send_sitting_reminder"] = False
    else:
        print "Calculating sitting reminder"
        reminders["send_sitting_reminder"] = get_sitting_reminder(
            current_session)

    if should_skip_posture_reminder_cycle(current_session):
        status_msg = ("Skipped Current Posture Reminder b/c " +
                      "user has seen posture reminder too recently")
        reminders["status"] = status_msg
        reminders["send_posture_reminder"] = False
    else:
        print "Calculating Posture reminder"
        reminders["send_posture_reminder"] = get_posture_reminder(
            current_session)

    reminders["status"] = "Calculated Current Reminders"

    return reminders


def should_skip_sitting_reminder_cycle(session):
    print "Last sitting reminder sent: " + str(session.last_sitting_reminder_sent)
    if session.last_sitting_reminder_sent is None:
        print "No sitting reminders have been sent"
        return False
    print "Calculating Sitting Reminder Skip Cycle Window"
    next_open_reminder_window = (
        session.last_sitting_reminder_sent
        + datetime.timedelta(seconds=config.MIN_INTERVAL_BETWEEN_SITTING_REMINDERS))
    should_skip = get_current_time_utc() < next_open_reminder_window
    print "Should skip sitting reminder: " + str(should_skip)
    return should_skip


def should_skip_posture_reminder_cycle(session):
    print "Last posture reminder sent: " + str(session.last_posture_reminder_sent)
    if session.last_posture_reminder_sent is None:
        print "No posture reminders have been sent"
        return False
    print "Calculating Posture Reminder Skip Cycle Window"
    next_open_reminder_window = (
        session.last_posture_reminder_sent
        + datetime.timedelta(seconds=config.MIN_INTERVAL_BETWEEN_POSTURE_REMINDERS))
    should_skip = get_current_time_utc() < next_open_reminder_window
    print "Should skip posture reminder: " + str(should_skip)
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
    print "POSTURE REMINDER_TRIGGERED: " + str(posture_reminder_triggered)
    user_still_sitting = session.last_sitting_signal_time > last_required_sitting_time
    print "USER STILL SITTING: " + str(user_still_sitting)
    return posture_reminder_triggered and user_still_sitting



def send_reminder(username, reminder_type):
    print "Sending reminder: %s" % reminder_type
    session = session_manager.get_users_current_session(username)
    if session is not None:
        if reminder_type == SITTING_EVENT:
            status_msg = "Sending SITTING reminder and updating last reminder time"
            session_manager.update_last_sitting_reminder_sent_time(session)
        elif reminder_type == POSTURE_EVENT:
            status_msg = "Sending POSTURE reminder and updating last reminder time"
            session_manager.update_last_posture_reminder_sent_time(session)
    else:
        status_msg = "No open sessions for user: %s" % username
    return status_msg

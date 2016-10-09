from app.sessions import session_manager


def close_stale_sessions():
    stale_sessions = session_manager.get_stale_sessions()
    for session in stale_sessions:
    	print "Closing session: %s" % str(session)
        session_manager.close_session(session)

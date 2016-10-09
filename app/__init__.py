import os
from flask import Flask
from flask.ext.cors import CORS
from app.database import db

# Initialize App
application = Flask(__name__)
CORS(application)
application.config.from_object(
    'app.config.' + os.getenv('SMART_CHAIR_CONFIG'))

# Initialize Logging
'''
from app.utils import logger
application.logger.addHandler(logger.get_rotating_file_handler(APP_LOG_FILE))
items_log = logger.get_logger(JOB_ITEMS_LOG_FILE, log_level=LOG_LEVEL)
tasks_log = logger.get_logger(TASKS_LOG_FILE,  log_level=LOG_LEVEL)
jobs_log = logger.get_logger(JOBS_LOG_FILE, log_level=LOG_LEVEL)
'''

# Import APIs
import app.users.api
import app.sessions.api
import app.reminders.api


@application.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

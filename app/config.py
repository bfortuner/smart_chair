import os
import logging


class Config(object):
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "secret" #os.getenv('SMART_CHAIR_APP_SECRET_KEY', 'secret')
    DB_ISOLATION_LEVEL = 'READ UNCOMMITTED'

class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SMART_CHAIR_DATABASE_URI')
    APP_LOG_LEVEL = logging.INFO
    MAIL_LOG_LEVEL = logging.ERROR
    CLIENT_AUTH_KEY = os.getenv('SMART_CHAIR_CLIENT_AUTH_KEY')
    MIN_INTERVAL_BETWEEN_SITTING_REMINDERS=int(os.getenv('MIN_INTERVAL_BETWEEN_SITTING_REMINDERS'))
    MIN_INTERVAL_BETWEEN_POSTURE_REMINDERS=int(os.getenv('MIN_INTERVAL_BETWEEN_POSTURE_REMINDERS'))

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SMART_CHAIR_DATABASE_URI')
    # 'sqlite:///database.db' SQLite doesn't play well w SQLAlchemy :(
    APP_LOG_LEVEL = logging.DEBUG
    MAIL_LOG_LEVEL = logging.ERROR
    CLIENT_AUTH_KEY = 'testing'
    MIN_INTERVAL_BETWEEN_SITTING_REMINDERS = 60
    MIN_INTERVAL_BETWEEN_POSTURE_REMINDERS = 20


config = globals()[os.getenv('SMART_CHAIR_CONFIG', 'TestConfig')]
print config.MIN_INTERVAL_BETWEEN_SITTING_REMINDERS
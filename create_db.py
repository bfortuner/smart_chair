from app.database import db, init_db
from app.sessions.models import Session
from app.users.models import User
from app.users.constants import ADMIN_USERNAME
from app.events.constants import SITTING_EVENT, POSTURE_EVENT 
import datetime

"""
DO NOT RUN THIS SCRIPT IN ''PROD'' IF DATABASE ALREADY HAS LIVE DATA!
"""

# # Drop and recreate DB
init_db()

print "DB tables created"

# # Insert Admin User
admin_user = User(ADMIN_USERNAME)
db.add(admin_user)
db.commit()

print "User table loaded"


print "Event Tracking Status Types loaded"

# # Insert Test Event
# current_time = datetime.datetime.now()
# event_complete = Event(User.query.filter_by(
#     username=ADMIN_USERNAME).first().id,
#     current_time, SEIZURE_EVENT_TYPE, 4, "1-3", 'COMPLETE')
# event_complete1 = Event(User.query.filter_by(
#     username=ADMIN_USERNAME).first().id,
#     current_time, SEIZURE_EVENT_TYPE, 3, "1-3", 'COMPLETE')
# event_complete2 = Event(User.query.filter_by(
#     username=ADMIN_USERNAME).first().id,
#     current_time - datetime.timedelta(days=5), SEIZURE_EVENT_TYPE, 2, "1-3", 'COMPLETE')
# event_complete3 = Event(User.query.filter_by(
#     username=ADMIN_USERNAME).first().id,
#     current_time - datetime.timedelta(days=5), AURA_EVENT_TYPE, 1, "1-3", 'COMPLETE')
# event_complete4 = Event(User.query.filter_by(
#     username=ADMIN_USERNAME).first().id,
#     current_time - datetime.timedelta(days=15), SEIZURE_EVENT_TYPE, 2, "1-3", 'COMPLETE')
# event_incomplete = Event(User.query.filter_by(
#     username=ADMIN_USERNAME).first().id)
# db.add(event_complete)
# db.add(event_complete1)
# db.add(event_complete2)
# # db.add(event_complete3)
# # db.add(event_complete4)
# # db.add(event_incomplete)
# db.commit()



print "Session table loaded"

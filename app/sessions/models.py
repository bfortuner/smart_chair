from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from datetime import datetime


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), ForeignKey('users.username'), nullable=False)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime)
    last_sitting_signal_time = Column(DateTime, default=func.now())
    last_posture_signal_time = Column(DateTime, default=func.now())

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return ('<SessionId: %r, '
                'User:%s, '
                'StartTime:%s, '
                'EndTime:%s, '
                'LastSittingTime:%s, '
                'LastPostureTime:%s' % (self.id, self.username, self.start_time,
            self.end_time, self.last_sitting_signal_time, self.last_posture_signal_time))

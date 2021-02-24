from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class TapRecord(Base):
    __tablename__ = 'taprecords'
    # date = Column(DateTime, primary_key=True, default=datetime.now())
    id = Column(Integer, primary_key=True)
    name = Column(String)
    error_count = Column(Integer)
    sentence_length = Column(Integer)
    timestamps = Column(String)
    keys = Column(String)
    joy_sadness = Column(Integer)
    anger_fear = Column(Integer)
    trust_disgust = Column(Integer)
    interest_distraction = Column(Integer)
    impression_pessimism = Column(Integer)

    def __init__(self, error_count=None, timestamps=None, keys=None, name=None, \
        sentence_length=None, joy_sadness=None, anger_fear=None, trust_disgust=None, \
        interest_distraction=None, impression_pessimism=None):
        self.name = name
        self.error_count = error_count
        self.timestamps = timestamps
        self.keys = keys
        self.sentence_length = sentence_length
        self.joy_sadness = joy_sadness
        self.anger_fear = anger_fear
        self.trust_disgust = trust_disgust
        self.interest_distraction = interest_distraction
        self.impression_pessimism = impression_pessimism

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
    joy_sadness = Column(Integer)
    anger_fear = Column(Integer)

    def __init__(self, error_count=None, timestamps=None, name=None, sentence_length=None, joy_sadness=None, anger_fear=None):
        self.name = name
        self.error_count = error_count
        self.timestamps = timestamps
        self.sentence_length = sentence_length
        self.joy_sadness = joy_sadness
        self.anger_fear = anger_fear

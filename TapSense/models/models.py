from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class TapRecord(Base):
    __tablename__ = 'taprecords'
    # date = Column(DateTime, primary_key=True, default=datetime.now())
    id = Column(Integer, primary_key=True)
    name = Column(String)
    emotion = Column(String)
    error_count = Column(Integer)
    timestamps = Column(String)

    def __init__(self, error_count=None, timestamps=None, name=None, emotion=None):
        self.name = name
        self.emotion = emotion
        self.error_count = error_count
        self.timestamps = timestamps

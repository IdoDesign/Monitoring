from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from base import Base
import uuid
from datetime import datetime
class Heartbeat(Base):
    __tablename__ = 'heartbeats'
    _id = Column(String(250), primary_key=True)
    checkname = Column(String, nullable=False)
    hostname = Column(String, nullable=False) 
    timestamp = Column(DateTime, nullable=False)
    result = Column(Boolean, nullable=False)
    response_time = Column(Float, nullable=False)
    
    def __init__(self, checkname, hostname, result, response_time, time=None, _id=None) -> None:
        self._id = uuid.uuid4().hex if _id is None else _id
        self.checkname = checkname
        self.hostname = hostname
        self.timestamp = datetime.utcnow() if time is None else time
        self.result = result
        self.response_time = response_time
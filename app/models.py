from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    miss_time = Column(Integer, default="0")
    station_id = Column(String(30), nullable=False)
    bus_id = Column(String(30), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    

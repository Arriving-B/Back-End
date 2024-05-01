from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Station(Base):
    __tablename__ = "station"

    id = Column(String(30), primary_key=True)
    name = Column(String(20), nullable=False)
    city = Column(Integer, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

class Bus(Base):
    __tablename__ = "bus"

    id = Column(String(30), primary_key=True)
    type = Column(String(4), nullable=False)
    area = Column(String(10))
    num = Column(String(10), nullable=False)
    sp_id = Column(String(30), ForeignKey("station.id"))
    ep_id = Column(String(30), ForeignKey("station.id"))
    fd_time = Column(Time)
    ld_time = Column(Time)
    interval_time = Column(Integer)
    interval_haltime = Column(Integer)

    station = relationship("Station", backref="buses")

class Bus_Station(Base):
    __tablename__ = "bus-station"

    station_id = Column(String(30), ForeignKey("station.id"), primary_key=True)
    bus_id = Column(String(30), ForeignKey("bus.id"), primary_key=True)
    miss_time = Column(Integer, nullable=False, default=0)

    station = relationship("Station", backref="bss")
    bus = relationship("Bus", backref="bss")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    miss_time = Column(Integer, nullable=False)
    station_id = Column(String(30), ForeignKey("station.id"))
    bus_id = Column(String(30), ForeignKey("bus.id"))

    station = relationship("Station", backref="feedbacks")
    bus = relationship("Bus", backref="feedbacks")
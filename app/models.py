from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Route(Base):
    __tablename__ = "route"
    
    station_id = Column("station_id", ForeignKey("station.id"), primary_key=True)
    bus_id = Column("bus_id", ForeignKey("bus.id"), primary_key=True)
    miss_time = Column(Integer, default="0")

    feedbacks = relationship("Feedback", back_populates="route")

class Station(Base):
    __tablename__ = "station"

    id = Column(String(30), primary_key=True, unique=True)
    name = Column(String(20), nullable=False)
    city = Column(Integer, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    starting_buses = relationship("Bus", back_populates="start_station", lazy="dynamic", foreign_keys="[Bus.sp_id]")
    ending_buses = relationship("Bus", back_populates="end_station", lazy="dynamic", foreign_keys="[Bus.ep_id]")
    buses = relationship("Bus", secondary="route", back_populates="stations")

class Bus(Base):
    __tablename__ = "bus"

    id = Column(String(30), primary_key=True, unique=True)
    type = Column(String(4), nullable=False)
    area = Column(String(10))
    num = Column(String(10), nullable=False)
    sp_id = Column(String(30), ForeignKey("station.id"), nullable=False)
    ep_id = Column(String(30), ForeignKey("station.id"), nullable=False)
    fd_time = Column(Time)
    ld_time = Column(Time)
    interval_time = Column(Integer)
    interval_haltime = Column(Integer)

    start_station = relationship("Station", foreign_keys=[sp_id], back_populates="starting_buses", lazy="dynamic")
    end_station = relationship("Station", foreign_keys=[ep_id], back_populates="ending_buses", lazy="dynamic")
    stations = relationship("Station", secondary="route", back_populates="buses")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    miss_time = Column(Integer, default="0")
    station_id = Column(String(30), ForeignKey("station.id"), nullable=False)
    bus_id = Column(String(30), ForeignKey("bus.id"), nullable=False)

    route = relationship("Route", back_populates="feedbacks")

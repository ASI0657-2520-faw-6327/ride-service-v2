from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.infrastructure.db.base import Base


class RideStatusDB(str, PyEnum):
    OPEN = "OPEN"
    FULL = "FULL"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PassengerStatusDB(str, PyEnum):
    JOINED = "JOINED"
    CANCELLED = "CANCELLED"


class RideModel(Base):
    __tablename__ = "rides"

    id = Column(String, primary_key=True, index=True)
    driver_id = Column(String, index=True, nullable=False)
    origin = Column(String, index=True, nullable=False)
    destination = Column(String, index=True, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    seats_total = Column(Integer, nullable=False)
    seats_available = Column(Integer, nullable=False)
    status = Column(Enum(RideStatusDB), default=RideStatusDB.OPEN, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    passengers = relationship("RidePassengerModel", back_populates="ride")


class RidePassengerModel(Base):
    __tablename__ = "ride_passengers"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(String, ForeignKey("rides.id"), nullable=False)
    passenger_id = Column(String, index=True, nullable=False)
    status = Column(Enum(PassengerStatusDB), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime, nullable=True)

    ride = relationship("RideModel", back_populates="passengers")

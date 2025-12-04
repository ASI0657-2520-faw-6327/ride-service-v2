from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class RideStatus(str, Enum):
    OPEN = "OPEN"
    FULL = "FULL"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PassengerStatus(str, Enum):
    JOINED = "JOINED"
    CANCELLED = "CANCELLED"


@dataclass
class Ride:
    id: Optional[int]
    driver_id: str
    origin: str
    destination: str
    departure_time: datetime
    seats_total: int
    seats_available: int
    status: RideStatus
    created_at: datetime
    updated_at: datetime


@dataclass
class RidePassenger:
    id: Optional[int]
    ride_id: int
    passenger_id: str
    status: PassengerStatus
    joined_at: datetime
    left_at: Optional[datetime]

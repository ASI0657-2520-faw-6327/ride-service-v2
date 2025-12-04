from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.entities import RideStatus

@dataclass
class CreateRideCommand:
    driver_id: str
    origin: str
    destination: str
    departure_time: datetime
    seats_total: int


@dataclass
class JoinRideCommand:
    ride_id: int
    passenger_id: str


@dataclass
class ListRidesQuery:
    origin: Optional[str] = None
    destination: Optional[str] = None
    status: Optional[RideStatus] = None

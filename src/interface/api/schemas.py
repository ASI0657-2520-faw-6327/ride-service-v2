from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.domain.entities import RideStatus, PassengerStatus


class RideBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    seats_total: int = Field(gt=0)


class CreateRideRequest(RideBase):
    """Los datos del ride; el driver sale del token JWT."""
    pass


class RideResponse(RideBase):
    id: int
    driver_id: str
    seats_available: int
    status: RideStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RidePassengerResponse(BaseModel):
    id: int
    ride_id: int
    passenger_id: str
    status: PassengerStatus
    joined_at: datetime
    left_at: Optional[datetime]


class ListRidesResponse(BaseModel):
    rides: List[RideResponse]

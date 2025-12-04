from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain.entities import Ride, RidePassenger, RideStatus


class RideRepositoryPort(ABC):
    @abstractmethod
    def create_ride(self, ride: Ride) -> Ride:
        raise NotImplementedError

    @abstractmethod
    def get_ride_by_id(self, ride_id: int) -> Optional[Ride]:
        raise NotImplementedError

    @abstractmethod
    def save_ride(self, ride: Ride) -> Ride:
        raise NotImplementedError

    @abstractmethod
    def list_rides(
        self,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        status: Optional[RideStatus] = None,
        departure_from: Optional[datetime] = None,
    ) -> List[Ride]:
        raise NotImplementedError

    @abstractmethod
    def add_passenger(self, passenger: RidePassenger) -> RidePassenger:
        raise NotImplementedError

    @abstractmethod
    def get_passenger(
        self, ride_id: int, passenger_id: str
    ) -> Optional[RidePassenger]:
        raise NotImplementedError

    @abstractmethod
    def list_passengers(self, ride_id: int) -> List[RidePassenger]:
        raise NotImplementedError

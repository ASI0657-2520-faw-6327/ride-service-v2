from datetime import datetime

from src.application.dto import CreateRideCommand
from src.application.ports.ride_repository_port import RideRepositoryPort
from src.domain.entities import Ride, RideStatus


class CreateRideUseCase:
    def __init__(self, ride_repository: RideRepositoryPort) -> None:
        self._ride_repository = ride_repository

    def execute(self, command: CreateRideCommand) -> Ride:
        now = datetime.utcnow()
        ride = Ride(
            id=None,
            driver_id=command.driver_id,
            origin=command.origin,
            destination=command.destination,
            departure_time=command.departure_time,
            seats_total=command.seats_total,
            seats_available=command.seats_total,
            status=RideStatus.OPEN,
            created_at=now,
            updated_at=now,
        )
        return self._ride_repository.create_ride(ride)

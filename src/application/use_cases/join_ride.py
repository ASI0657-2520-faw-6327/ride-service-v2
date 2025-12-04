from datetime import datetime

from src.application.dto import JoinRideCommand
from src.application.ports.ride_repository_port import RideRepositoryPort
from src.domain.entities import (
    Ride,
    RidePassenger,
    RideStatus,
    PassengerStatus,
)


class RideNotFoundError(Exception):
    pass


class RideIsFullError(Exception):
    pass


class PassengerAlreadyJoinedError(Exception):
    pass


class JoinRideUseCase:
    def __init__(self, ride_repository: RideRepositoryPort) -> None:
        self._ride_repository = ride_repository

    def execute(self, command: JoinRideCommand) -> Ride:
        ride = self._ride_repository.get_ride_by_id(command.ride_id)
        if ride is None:
            raise RideNotFoundError("Ride not found")

        if ride.status != RideStatus.OPEN:
            raise RideIsFullError("Ride is not open")

        if ride.seats_available <= 0:
            raise RideIsFullError("Ride is full")

        existing = self._ride_repository.get_passenger(
            ride_id=ride.id, passenger_id=command.passenger_id  # type: ignore[arg-type]
        )
        if existing is not None and existing.status == PassengerStatus.JOINED:
            raise PassengerAlreadyJoinedError("Passenger already joined this ride")

        now = datetime.utcnow()
        passenger = RidePassenger(
            id=None,
            ride_id=ride.id,  # type: ignore[arg-type]
            passenger_id=command.passenger_id,
            status=PassengerStatus.JOINED,
            joined_at=now,
            left_at=None,
        )
        self._ride_repository.add_passenger(passenger)

        ride.seats_available -= 1

        if ride.seats_available == 0:
            ride.status = RideStatus.FULL

        ride.updated_at = now

        self._ride_repository.save_ride(ride)
        return ride

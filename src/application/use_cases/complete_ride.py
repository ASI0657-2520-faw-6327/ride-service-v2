from datetime import datetime

from src.application.ports.ride_repository_port import RideRepositoryPort
from src.domain.entities import RideStatus


class CompleteRideUseCase:
    def __init__(self, ride_repository: RideRepositoryPort) -> None:
        self._ride_repository = ride_repository

    def execute(self, ride_id: int) -> None:
        ride = self._ride_repository.get_ride_by_id(ride_id)
        if ride is None:
            raise ValueError("Ride not found")
        ride.status = RideStatus.COMPLETED
        ride.updated_at = datetime.utcnow()
        self._ride_repository.save_ride(ride)

from datetime import datetime
from typing import List, Optional

from src.application.dto import ListRidesQuery
from src.application.ports.ride_repository_port import RideRepositoryPort
from src.domain.entities import Ride


class ListRidesUseCase:
    def __init__(self, ride_repository: RideRepositoryPort) -> None:
        self._ride_repository = ride_repository

    def execute(self, query: Optional[ListRidesQuery] = None) -> List[Ride]:
        query = query or ListRidesQuery()
        return self._ride_repository.list_rides(
            origin=query.origin,
            destination=query.destination,
            status=query.status,
            departure_from=None,
        )

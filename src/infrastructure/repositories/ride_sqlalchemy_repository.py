from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.application.ports.ride_repository_port import RideRepositoryPort
from src.domain.entities import (
    Ride,
    RidePassenger,
    RideStatus,
    PassengerStatus,
)
from src.infrastructure.db.models import (
    RideModel,
    RidePassengerModel,
    RideStatusDB,
    PassengerStatusDB,
)


class RideSQLAlchemyRepository(RideRepositoryPort):
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_domain_ride(model: RideModel) -> Ride:
        return Ride(
            id=model.id,
            driver_id=model.driver_id,
            origin=model.origin,
            destination=model.destination,
            departure_time=model.departure_time,
            seats_total=model.seats_total,
            seats_available=model.seats_available,
            status=RideStatus(model.status.value),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_domain_passenger(model: RidePassengerModel) -> RidePassenger:
        return RidePassenger(
            id=model.id,
            ride_id=model.ride_id,
            passenger_id=model.passenger_id,
            status=PassengerStatus(model.status.value),
            joined_at=model.joined_at,
            left_at=model.left_at,
        )

    def create_ride(self, ride: Ride) -> Ride:
        db_ride = RideModel(
            driver_id=ride.driver_id,
            origin=ride.origin,
            destination=ride.destination,
            departure_time=ride.departure_time,
            seats_total=ride.seats_total,
            seats_available=ride.seats_available,
            status=RideStatusDB(ride.status.value),
            created_at=ride.created_at,
            updated_at=ride.updated_at,
        )
        self._session.add(db_ride)
        self._session.commit()
        self._session.refresh(db_ride)
        return self._to_domain_ride(db_ride)

    def get_ride_by_id(self, ride_id: int) -> Optional[Ride]:
        stmt = select(RideModel).where(RideModel.id == ride_id)
        result = self._session.execute(stmt).scalar_one_or_none()
        if result is None:
            return None
        return self._to_domain_ride(result)

    def save_ride(self, ride: Ride) -> Ride:
        db_ride: RideModel | None = self._session.get(RideModel, ride.id)
        if db_ride is None:
            raise ValueError("Ride not found in DB")

        db_ride.origin = ride.origin
        db_ride.destination = ride.destination
        db_ride.departure_time = ride.departure_time
        db_ride.seats_total = ride.seats_total
        db_ride.seats_available = ride.seats_available
        db_ride.status = RideStatusDB(ride.status.value)
        db_ride.updated_at = ride.updated_at

        self._session.commit()
        self._session.refresh(db_ride)
        return self._to_domain_ride(db_ride)

    def list_rides(
        self,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        status: Optional[RideStatus] = None,
        departure_from: Optional[datetime] = None,
    ) -> List[Ride]:
        filters = []
        if origin:
            filters.append(RideModel.origin == origin)
        if destination:
            filters.append(RideModel.destination == destination)
        if status:
            filters.append(RideModel.status == RideStatusDB(status.value))
        if departure_from:
            filters.append(RideModel.departure_time >= departure_from)

        stmt = select(RideModel)
        if filters:
            stmt = stmt.where(and_(*filters))

        results = self._session.execute(stmt).scalars().all()

        print(results)

        return [self._to_domain_ride(r) for r in results]

    def add_passenger(self, passenger: RidePassenger) -> RidePassenger:
        db_passenger = RidePassengerModel(
            ride_id=passenger.ride_id,
            passenger_id=passenger.passenger_id,
            status=PassengerStatusDB(passenger.status.value),
            joined_at=passenger.joined_at,
            left_at=passenger.left_at,
        )
        self._session.add(db_passenger)
        self._session.commit()
        self._session.refresh(db_passenger)
        return self._to_domain_passenger(db_passenger)

    def get_passenger(
        self,
        ride_id: int,
        passenger_id: str,
    ) -> Optional[RidePassenger]:
        stmt = select(RidePassengerModel).where(
            and_(
                RidePassengerModel.ride_id == ride_id,
                RidePassengerModel.passenger_id == passenger_id,
            )
        )
        result = self._session.execute(stmt).scalar_one_or_none()
        if result is None:
            return None
        return self._to_domain_passenger(result)

    def list_passengers(self, ride_id: int) -> List[RidePassenger]:
        stmt = select(RidePassengerModel).where(RidePassengerModel.ride_id == ride_id)
        results = self._session.execute(stmt).scalars().all()
        return [self._to_domain_passenger(p) for p in results]

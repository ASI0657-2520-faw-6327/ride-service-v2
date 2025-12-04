from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto import CreateRideCommand, JoinRideCommand, ListRidesQuery
from src.application.use_cases.create_ride import CreateRideUseCase
from src.application.use_cases.join_ride import (
    JoinRideUseCase,
    RideNotFoundError,
    RideIsFullError,
    PassengerAlreadyJoinedError,
)
from src.application.use_cases.list_rides import ListRidesUseCase
from src.application.use_cases.complete_ride import CompleteRideUseCase
from src.domain.entities import RideStatus
from src.interface.api.schemas import (
    CreateRideRequest,
    RideResponse,
    ListRidesResponse,
)
from src.interface.api.dependencies import (
    get_create_ride_uc,
    get_join_ride_uc,
    get_list_rides_uc,
    get_complete_ride_uc,
    get_current_user,
    AuthUser,
)

router = APIRouter(prefix="/rides", tags=["rides"])


@router.post(
    "",
    response_model=RideResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ride(
    body: CreateRideRequest,
    current_user: AuthUser = Depends(get_current_user),
    use_case: CreateRideUseCase = Depends(get_create_ride_uc),
) -> RideResponse:
    # Solo rol DRIVER puede crear rides
    if "DRIVER" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only drivers can create rides",
        )

    command = CreateRideCommand(
        driver_id=current_user.user_id,
        origin=body.origin,
        destination=body.destination,
        departure_time=body.departure_time,
        seats_total=body.seats_total,
    )
    ride = use_case.execute(command)
    return RideResponse(**ride.__dict__)


@router.post(
    "/{ride_id}/join",
    response_model=RideResponse,
)
def join_ride(
    ride_id: int,
    current_user: AuthUser = Depends(get_current_user),
    use_case: JoinRideUseCase = Depends(get_join_ride_uc),
) -> RideResponse:
    # Solo rol STUDENT se sube como pasajero
    if "STUDENT" not in current_user.roles :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can join rides as passengers",
        )

    command = JoinRideCommand(
        ride_id=ride_id,
        passenger_id=current_user.user_id,
    )
    try:
        ride = use_case.execute(command)
    except RideNotFoundError:
        raise HTTPException(status_code=404, detail="Ride not found")
    except RideIsFullError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PassengerAlreadyJoinedError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RideResponse(**ride.__dict__)


@router.get(
    "",
    response_model=ListRidesResponse,
)
def list_rides(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    status_filter: Optional[RideStatus] = None,
    use_case: ListRidesUseCase = Depends(get_list_rides_uc),
    _: AuthUser = Depends(get_current_user),  # cualquier usuario autenticado
) -> ListRidesResponse:
    query = ListRidesQuery(
        origin=origin,
        destination=destination,
        status=status_filter,
    )
    rides = use_case.execute(query)
    print(rides)
    return ListRidesResponse(
        rides=[RideResponse(**r.__dict__) for r in rides]
    )


@router.post(
    "/{ride_id}/complete",
    status_code=status.HTTP_204_NO_CONTENT,
)
def complete_ride(
    ride_id: int,
    current_user: AuthUser = Depends(get_current_user),
    use_case: CompleteRideUseCase = Depends(get_complete_ride_uc),
) -> None:
    # Solo el driver debería poder marcar su ride como completado (simple check aquí)
    # En un caso real: verificar que current_user.user_id == ride.driver_id
    # (habría que obtener el ride del repo; aquí lo dejamos simple por tamaño)
    if "DRIVER" not in current_user.roles :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only drivers can complete rides",
        )

    try:
        use_case.execute(ride_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ride not found")

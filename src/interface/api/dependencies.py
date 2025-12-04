from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException, status
from jwt import PyJWTError
from sqlalchemy.orm import Session

from src.config import settings
from src.infrastructure.db.session import get_db_session
from src.infrastructure.repositories.ride_sqlalchemy_repository import (
    RideSQLAlchemyRepository,
)
from src.application.use_cases.create_ride import CreateRideUseCase
from src.application.use_cases.join_ride import JoinRideUseCase
from src.application.use_cases.list_rides import ListRidesUseCase
from src.application.use_cases.complete_ride import CompleteRideUseCase


# ---------- DB ----------
def get_db() -> Generator[Session, None, None]:
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


def get_ride_repository(
    db: Session = Depends(get_db),
) -> RideSQLAlchemyRepository:
    return RideSQLAlchemyRepository(db)


# ---------- JWT / Auth ----------
@dataclass
class AuthUser:
    user_id: str
    roles: list[str] | None = None 


def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
) -> AuthUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    token = authorization.split(" ", 1)[1]

    options = {"verify_aud": settings.JWT_AUDIENCE is not None}
    try:
        decode_kwargs = {
            "key": settings.IAM_PUBLIC_KEY,
            "algorithms": [settings.JWT_ALGORITHM],
            "options": options,
        }
        if settings.JWT_ISSUER:
            decode_kwargs["issuer"] = settings.JWT_ISSUER
        if settings.JWT_AUDIENCE:
            decode_kwargs["audience"] = settings.JWT_AUDIENCE

        payload = jwt.decode(token, **decode_kwargs)  # type: ignore[arg-type]

    except PyJWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    roles_claim = payload.get("roles")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'sub' claim",
        )

    if roles_claim is None:
        roles_list: list[str] = []
    elif isinstance(roles_claim,str):
        roles_list = [roles_claim]
    else:
        roles_list = [ str(r) for r in roles_claim ]

    print(payload) 

    return AuthUser(user_id=user_id, roles=roles_list)


# ---------- Use Cases ----------
def get_create_ride_uc(
    repo: RideSQLAlchemyRepository = Depends(get_ride_repository),
) -> CreateRideUseCase:
    return CreateRideUseCase(repo)


def get_join_ride_uc(
    repo: RideSQLAlchemyRepository = Depends(get_ride_repository),
) -> JoinRideUseCase:
    return JoinRideUseCase(repo)


def get_list_rides_uc(
    repo: RideSQLAlchemyRepository = Depends(get_ride_repository),
) -> ListRidesUseCase:
    return ListRidesUseCase(repo)


def get_complete_ride_uc(
    repo: RideSQLAlchemyRepository = Depends(get_ride_repository),
) -> CompleteRideUseCase:
    return CompleteRideUseCase(repo)

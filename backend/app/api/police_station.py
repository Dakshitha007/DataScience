from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.auth.dependencies import require_admin
from app.database.session import get_db
from app.models.user import User

from app.schemas.police_station import (
    PoliceStationCreate,
    PoliceStationUpdate,
    PoliceStationResponse,
)

from app.services.police_station_service import (
    get_station_by_code,
    get_station_by_id,
    get_all_stations,
    create_station,
    update_station,
    delete_station,
)

router = APIRouter(
    prefix="/police-stations",
    tags=["Police Stations"]
)


@router.post(
    "/",
    response_model=PoliceStationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_station(
    station: PoliceStationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing_station = get_station_by_code(
        db,
        station.station_code,
    )

    if existing_station:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Station code already exists",
        )

    return create_station(
        db,
        station,
    )


@router.get(
    "/",
    response_model=List[PoliceStationResponse],
)
def get_stations(
    db: Session = Depends(get_db),
):
    return get_all_stations(db)


@router.get(
    "/{station_id}",
    response_model=PoliceStationResponse,
)
def get_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    station = get_station_by_id(
        db,
        station_id,
    )

    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Police station not found",
        )

    return station


@router.put(
    "/{station_id}",
    response_model=PoliceStationResponse,
)
def update_existing_station(
    station_id: int,
    station: PoliceStationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_station = get_station_by_id(
        db,
        station_id,
    )

    if not db_station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Police station not found",
        )

    if (
        station.station_code
        and station.station_code != db_station.station_code
    ):
        existing_station = get_station_by_code(
            db,
            station.station_code,
        )

        if existing_station:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Station code already exists",
            )

    return update_station(
        db,
        db_station,
        station,
    )


@router.delete(
    "/{station_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_station(
    station_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_station = get_station_by_id(
        db,
        station_id,
    )

    if not db_station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Police station not found",
        )

    delete_station(
        db,
        db_station,
    )

    return None
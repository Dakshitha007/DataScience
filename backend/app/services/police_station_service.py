from sqlalchemy.orm import Session

from app.models.police_station import PoliceStation
from app.schemas.police_station import (
    PoliceStationCreate,
    PoliceStationUpdate,
)


def get_station_by_code(
    db: Session,
    station_code: str
):
    return (
        db.query(PoliceStation)
        .filter(PoliceStation.station_code == station_code)
        .first()
    )


def get_station_by_id(
    db: Session,
    station_id: int
):
    return (
        db.query(PoliceStation)
        .filter(PoliceStation.id == station_id)
        .first()
    )


def get_all_stations(db: Session):
    return (
        db.query(PoliceStation)
        .order_by(PoliceStation.station_name)
        .all()
    )


def create_station(
    db: Session,
    station: PoliceStationCreate
):
    db_station = PoliceStation(
        station_code=station.station_code,
        station_name=station.station_name,
        district=station.district,
        city=station.city,
        address=station.address,
        phone=station.phone,
        latitude=station.latitude,
        longitude=station.longitude,
    )

    db.add(db_station)
    db.commit()
    db.refresh(db_station)

    return db_station


def update_station(
    db: Session,
    db_station: PoliceStation,
    station: PoliceStationUpdate
):
    update_data = station.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_station, key, value)

    db.commit()
    db.refresh(db_station)

    return db_station


def delete_station(
    db: Session,
    db_station: PoliceStation
):
    db.delete(db_station)
    db.commit()
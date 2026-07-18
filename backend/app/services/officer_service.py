from sqlalchemy.orm import Session

from app.models.officer import Officer
from app.schemas.officer import OfficerCreate


def get_officer_by_badge(db: Session, badge_number: str):
    return (
        db.query(Officer)
        .filter(Officer.badge_number == badge_number)
        .first()
    )


def get_officer_by_user_id(db: Session, user_id: int):
    return (
        db.query(Officer)
        .filter(Officer.user_id == user_id)
        .first()
    )


def create_officer(
    db: Session,
    officer: OfficerCreate
):
    db_officer = Officer(
        user_id=officer.user_id,
        badge_number=officer.badge_number,
        name=officer.name,
        designation=officer.designation.value,
        station=officer.station,
        phone=officer.phone
    )

    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)

    return db_officer
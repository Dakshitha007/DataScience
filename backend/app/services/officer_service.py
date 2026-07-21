from sqlalchemy.orm import Session

from app.models.officer import Officer
from app.schemas.officer import OfficerCreate, OfficerUpdate


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


def get_officer(db: Session, officer_id: int):
    return (
        db.query(Officer)
        .filter(Officer.id == officer_id)
        .first()
    )


def get_all_officers(db: Session):
    return db.query(Officer).all()


def create_officer(db: Session, officer: OfficerCreate):
    db_officer = Officer(**officer.model_dump())

    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)

    return db_officer


def update_officer(
    db: Session,
    db_officer: Officer,
    officer_update: OfficerUpdate,
):
    update_data = officer_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_officer, key, value)

    db.commit()
    db.refresh(db_officer)

    return db_officer


def delete_officer(
    db: Session,
    db_officer: Officer,
):
    db.delete(db_officer)
    db.commit()
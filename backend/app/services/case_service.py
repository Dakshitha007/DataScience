from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.user import User
from app.models.officer import Officer

from app.schemas.case import CaseCreate, CaseUpdate
from app.utils.enums import AppRole, Designation


def get_accessible_cases(
    db: Session,
    current_user: User,
    current_officer: Officer | None
):
    # Admin -> Every case
    if current_user.role == AppRole.ADMIN.value:
        return db.query(Case).all()

    # Inspector -> Cases from their station
    if current_officer.designation == Designation.INSPECTOR.value:
        return (
            db.query(Case)
            .filter(
                Case.station == current_officer.station
            )
            .all()
        )

    # Sub Inspector -> Assigned cases only
    return (
        db.query(Case)
        .filter(
            Case.officer_id == current_officer.id
        )
        .all()
    )


def authorize_case_access(
    db: Session,
    case_id: int,
    current_user: User,
    current_officer: Officer | None
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )

    # Admin -> Full access
    if current_user.role == AppRole.ADMIN.value:
        return case

    # Inspector -> Same station only
    if current_officer.designation == Designation.INSPECTOR.value:
        if case.station != current_officer.station:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return case

    # Sub Inspector -> Assigned cases only
    if case.officer_id != current_officer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return case


def validate_officer_assignment(
    db: Session,
    officer_id: int,
    current_user: User,
    current_officer: Officer | None
):
    assigned_officer = (
        db.query(Officer)
        .filter(Officer.id == officer_id)
        .first()
    )

    if assigned_officer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned officer not found."
        )

    # Admin -> Can assign anyone
    if current_user.role == AppRole.ADMIN.value:
        return assigned_officer

    # Inspector -> Same station only
    if assigned_officer.station != current_officer.station:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can assign cases only to officers in your station."
        )

    return assigned_officer


def get_case_by_id(
    db: Session,
    case_id: int
):
    return (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )


def create_case(
    db: Session,
    case: CaseCreate
):
    db_case = Case(
        case_number=case.case_number,
        title=case.title,
        description=case.description,
        status=case.status,
        priority=case.priority,
        station=case.station,
        officer_id=case.officer_id
    )

    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    return db_case


def update_case(
    db: Session,
    case_id: int,
    case_update: CaseUpdate
):
    db_case = get_case_by_id(
        db,
        case_id
    )

    if not db_case:
        return None

    update_data = case_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_case, key, value)

    db.commit()
    db.refresh(db_case)

    return db_case


def delete_case(
    db: Session,
    case_id: int
):
    db_case = get_case_by_id(
        db,
        case_id
    )

    if not db_case:
        return None

    db.delete(db_case)
    db.commit()

    return db_case
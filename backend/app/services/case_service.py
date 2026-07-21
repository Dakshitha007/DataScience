from fastapi import HTTPException, status
from sqlalchemy.orm import Query, Session

from app.models.case import Case
from app.models.case_assignment import CaseAssignment
from app.models.officer import Officer
from app.models.user import User

from app.schemas.case import CaseCreate, CaseUpdate

from app.utils.enums import (
    AppRole,
    OfficerRank,
)


def get_accessible_cases_query(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
) -> Query:
    """
    Returns only the cases accessible to the current user.
    """

    # Admin -> All cases
    if current_user.role == AppRole.ADMIN.value:
        return db.query(Case)

    if current_officer is None:
        return db.query(Case).filter(False)

    # Inspector -> All cases in same station
    if current_officer.rank == OfficerRank.INSPECTOR:
        return (
            db.query(Case)
            .filter(
                Case.police_station_id
                == current_officer.police_station_id
            )
        )

    # Other officers -> Assigned cases only
    return (
        db.query(Case)
        .join(
            CaseAssignment,
            CaseAssignment.case_id == Case.id,
        )
        .filter(
            CaseAssignment.officer_id == current_officer.id
        )
        .distinct()
    )


def get_accessible_cases(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    return (
        get_accessible_cases_query(
            db,
            current_user,
            current_officer,
        ).all()
    )


def authorize_case_access(
    db: Session,
    case_id: int,
    current_user: User,
    current_officer: Officer | None,
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    if current_user.role == AppRole.ADMIN.value:
        return case

    if current_officer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    if current_officer.rank == OfficerRank.INSPECTOR:
        if (
            case.police_station_id
            != current_officer.police_station_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        return case

    assignment = (
        db.query(CaseAssignment)
        .filter(
            CaseAssignment.case_id == case.id,
            CaseAssignment.officer_id == current_officer.id,
        )
        .first()
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return case
def get_case_by_id(
    db: Session,
    case_id: int,
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


def create_case(
    db: Session,
    case_data: CaseCreate,
):
    # Check duplicate Case Number
    existing_case = (
        db.query(Case)
        .filter(
            Case.case_number == case_data.case_number
        )
        .first()
    )

    if existing_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Case number already exists",
        )

    # Check duplicate FIR Number
    existing_fir = (
        db.query(Case)
        .filter(
            Case.fir_number == case_data.fir_number
        )
        .first()
    )

    if existing_fir:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="FIR number already exists",
        )

    new_case = Case(
        case_number=case_data.case_number,
        fir_number=case_data.fir_number,
        crime_type=case_data.crime_type,
        title=case_data.title,
        description=case_data.description,
        status=case_data.status,
        priority=case_data.priority,
        police_station_id=case_data.police_station_id,
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case
def update_case(
    db: Session,
    case_id: int,
    case_update: CaseUpdate,
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    update_data = case_update.model_dump(
        exclude_unset=True
    )

    # Check duplicate case number
    if "case_number" in update_data:
        existing_case = (
            db.query(Case)
            .filter(
                Case.case_number == update_data["case_number"],
                Case.id != case_id,
            )
            .first()
        )

        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Case number already exists",
            )

    # Check duplicate FIR number
    if "fir_number" in update_data:
        existing_fir = (
            db.query(Case)
            .filter(
                Case.fir_number == update_data["fir_number"],
                Case.id != case_id,
            )
            .first()
        )

        if existing_fir:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="FIR number already exists",
            )

    for key, value in update_data.items():
        setattr(case, key, value)

    db.commit()
    db.refresh(case)

    return case
def delete_case(
    db: Session,
    case_id: int,
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    db.delete(case)
    db.commit()

    return {
        "message": "Case deleted successfully"
    }
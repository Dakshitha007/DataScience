from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.case_criminal import CaseCriminal
from app.models.criminal import Criminal
from app.models.officer import Officer
from app.models.user import User


from app.services.case_service import (
    get_accessible_cases_query,
)
from app.auth.permissions import (
    require_criminal_create_permission,
    require_criminal_update_permission,
    require_criminal_delete_permission,
)
def create_criminal(
    db: Session,
    criminal: CriminalCreate,
    current_user: User,
    current_officer: Officer | None,
):
    require_criminal_create_permission(
        current_user,
        current_officer,
    )

    existing = (
        db.query(Criminal)
        .filter(
            Criminal.criminal_code == criminal.criminal_code
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Criminal code already exists",
        )

    db_criminal = Criminal(
        criminal_code=criminal.criminal_code,
        full_name=criminal.full_name,
        alias=criminal.alias,
        gender=criminal.gender,
        date_of_birth=criminal.date_of_birth,
        phone=criminal.phone,
        address=criminal.address,
        city=criminal.city,
        district=criminal.district,
        nationality=criminal.nationality,
        status=criminal.status,
    )

    db.add(db_criminal)
    db.commit()
    db.refresh(db_criminal)

    return db_criminal
def get_criminal_by_id(
    db: Session,
    criminal_id: int,
):
    criminal = (
        db.query(Criminal)
        .filter(
            Criminal.id == criminal_id
        )
        .first()
    )

    if criminal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criminal not found",
        )

    return criminal
def get_all_criminals(
    db: Session,
):
    criminals = (
        db.query(Criminal)
        .order_by(
            Criminal.created_at.desc()
        )
        .all()
    )

    return CriminalListResponse(
        criminals=[
            CriminalSummaryResponse.model_validate(c)
            for c in criminals
        ]
    )
def get_case_criminals(
    db: Session,
    case_id: int,
    current_user: User,
    current_officer: Officer | None,
):
    accessible_cases = (
        get_accessible_cases_query(
            db,
            current_user,
            current_officer,
        )
        .with_entities(Case.id)
        .subquery()
    )

    case_exists = (
        db.query(Case)
        .filter(
            Case.id == case_id,
            Case.id.in_(accessible_cases),
        )
        .first()
    )

    if case_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found or access denied",
        )

    criminals = (
        db.query(Criminal)
        .join(
            CaseCriminal,
            Criminal.id == CaseCriminal.criminal_id,
        )
        .filter(
            CaseCriminal.case_id == case_id
        )
        .all()
    )

    return CriminalListResponse(
        criminals=[
            CriminalSummaryResponse.model_validate(c)
            for c in criminals
        ]
    )
def search_criminals(
    db: Session,
    full_name: str | None = None,
    alias: str | None = None,
    status: str | None = None,
):
    query = db.query(Criminal)

    if full_name:
        query = query.filter(
            Criminal.full_name.ilike(f"%{full_name}%")
        )

    if alias:
        query = query.filter(
            Criminal.alias.ilike(f"%{alias}%")
        )

    if status:
        query = query.filter(
            Criminal.status == status
        )

    criminals = (
        query.order_by(
            Criminal.full_name
        )
        .all()
    )

    return CriminalListResponse(
        criminals=[
            CriminalSummaryResponse.model_validate(c)
            for c in criminals
        ]
    )
def update_criminal(
    db: Session,
    criminal_id: int,
    criminal_update: CriminalUpdate,
    current_user: User,
    current_officer: Officer | None,
):
    require_criminal_update_permission(
        current_user,
        current_officer,
    )

    criminal = (
        db.query(Criminal)
        .filter(
            Criminal.id == criminal_id
        )
        .first()
    )

    if criminal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criminal not found",
        )

    update_data = criminal_update.model_dump(
        exclude_unset=True
    )

    if (
        "criminal_code" in update_data
        and update_data["criminal_code"] != criminal.criminal_code
    ):
        exists = (
            db.query(Criminal)
            .filter(
                Criminal.criminal_code == update_data["criminal_code"]
            )
            .first()
        )

        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Criminal code already exists",
            )

    for key, value in update_data.items():
        setattr(criminal, key, value)

    db.commit()
    db.refresh(criminal)

    return criminal
def delete_criminal(
    db: Session,
    criminal_id: int,
    current_user: User,
):
    require_criminal_delete_permission(
        current_user,
    )

    criminal = (
        db.query(Criminal)
        .filter(
            Criminal.id == criminal_id
        )
        .first()
    )

    if criminal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criminal not found",
        )

    db.delete(criminal)
    db.commit()

    return {
        "message": "Criminal deleted successfully"
    }
def get_dashboard_summary(
    db: Session,
):
    query = db.query(Criminal)

    return CriminalDashboardResponse(
        total_criminals=query.count(),

        active=query.filter(
            Criminal.status == "Active"
        ).count(),

        arrested=query.filter(
            Criminal.status == "Arrested"
        ).count(),

        wanted=query.filter(
            Criminal.status == "Wanted"
        ).count(),

        released=query.filter(
            Criminal.status == "Released"
        ).count(),

        deceased=query.filter(
            Criminal.status == "Deceased"
        ).count(),
    )
def get_criminal_statistics(
    db: Session,
):
    query = db.query(Criminal)

    return CriminalStatisticsResponse(
        total_criminals=query.count(),

        male=query.filter(
            Criminal.gender == "Male"
        ).count(),

        female=query.filter(
            Criminal.gender == "Female"
        ).count(),

        other_gender=query.filter(
            Criminal.gender == "Other"
        ).count(),

        indian=query.filter(
            Criminal.nationality == "Indian"
        ).count(),

        foreign=query.filter(
            Criminal.nationality != "Indian"
        ).count(),
    )

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.officer import Officer
from app.models.user import User

from app.schemas.investigation import (
    CaseDetailsResponse,
    CaseSummaryResponse,
    InvestigationDashboardResponse,
    InvestigationStatisticsResponse,
    OfficerInfoResponse,
    OfficerWorkloadResponse,
    OfficerWorkloadsResponse,
    PendingCasesResponse,
    RecentCasesResponse,
    SearchCasesResponse,
)

from app.services.case_service import (
    authorize_case_access,
    get_accessible_cases_query,
)

from app.utils.enums import (
    AppRole,
    CasePriority,
    CaseStatus,
    Designation,
)


def get_dashboard_summary(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    query = get_accessible_cases_query(
        db,
        current_user,
        current_officer,
    )

    total_cases = query.count()

    open_cases = query.filter(
        Case.status == CaseStatus.OPEN.value
    ).count()

    closed_cases = query.filter(
        Case.status == CaseStatus.CLOSED.value
    ).count()

    under_investigation = query.filter(
        Case.status == CaseStatus.UNDER_INVESTIGATION.value
    ).count()

    high_priority = query.filter(
        Case.priority == CasePriority.HIGH.value
    ).count()

    return InvestigationDashboardResponse(
        total_cases=total_cases,
        open_cases=open_cases,
        closed_cases=closed_cases,
        under_investigation=under_investigation,
        high_priority=high_priority,
    )


def get_recent_cases(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
    limit: int = 10,
):
    query = get_accessible_cases_query(
        db,
        current_user,
        current_officer,
    )

    cases = (
        query.order_by(Case.created_at.desc())
        .limit(limit)
        .all()
    )

    return RecentCasesResponse(
        cases=[
            CaseSummaryResponse(
                id=case.id,
                case_number=case.case_number,
                title=case.title,
                status=case.status,
                priority=case.priority,
                station=case.station,
                created_at=case.created_at,
            )
            for case in cases
        ]
    )


def search_cases(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
    case_number: str | None = None,
    title: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    station: str | None = None,
):
    query = get_accessible_cases_query(
        db,
        current_user,
        current_officer,
    )

    if case_number:
        query = query.filter(
            Case.case_number.ilike(f"%{case_number}%")
        )

    if title:
        query = query.filter(
            Case.title.ilike(f"%{title}%")
        )

    if status:
        query = query.filter(
            Case.status == status
        )

    if priority:
        query = query.filter(
            Case.priority == priority
        )

    if station:
        query = query.filter(
            Case.station.ilike(f"%{station}%")
        )

    cases = (
        query.order_by(Case.created_at.desc())
        .all()
    )

    return SearchCasesResponse(
        cases=[
            CaseSummaryResponse(
                id=case.id,
                case_number=case.case_number,
                title=case.title,
                status=case.status,
                priority=case.priority,
                station=case.station,
                created_at=case.created_at,
            )
            for case in cases
        ]
    )


def get_pending_cases(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    query = get_accessible_cases_query(
        db,
        current_user,
        current_officer,
    )

    cases = (
        query.filter(
            Case.status.in_(
                [
                    CaseStatus.OPEN.value,
                    CaseStatus.UNDER_INVESTIGATION.value,
                ]
            )
        )
        .order_by(Case.created_at.desc())
        .all()
    )

    return PendingCasesResponse(
        cases=[
            CaseSummaryResponse(
                id=case.id,
                case_number=case.case_number,
                title=case.title,
                status=case.status,
                priority=case.priority,
                station=case.station,
                created_at=case.created_at,
            )
            for case in cases
        ]
    )


def get_investigation_statistics(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    query = get_accessible_cases_query(
        db,
        current_user,
        current_officer,
    )

    return InvestigationStatisticsResponse(
        total_cases=query.count(),
        open_cases=query.filter(
            Case.status == CaseStatus.OPEN.value
        ).count(),
        closed_cases=query.filter(
            Case.status == CaseStatus.CLOSED.value
        ).count(),
        under_investigation=query.filter(
            Case.status == CaseStatus.UNDER_INVESTIGATION.value
        ).count(),
        high_priority=query.filter(
            Case.priority == CasePriority.HIGH.value
        ).count(),
        medium_priority=query.filter(
            Case.priority == CasePriority.MEDIUM.value
        ).count(),
        low_priority=query.filter(
            Case.priority == CasePriority.LOW.value
        ).count(),
    )


def get_case_details(
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

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    authorize_case_access(
        case,
        current_user,
        current_officer,
    )

    return CaseDetailsResponse(
        id=case.id,
        case_number=case.case_number,
        title=case.title,
        description=case.description,
        status=case.status,
        priority=case.priority,
        station=case.station,
        officer=OfficerInfoResponse(
            id=case.officer.id,
            badge_number=case.officer.badge_number,
            name=case.officer.name,
            designation=case.officer.designation,
            station=case.officer.station,
        ),
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


def get_officer_workloads(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    officers_query = db.query(Officer)

    if current_user.role == AppRole.ADMIN.value:
        officers = officers_query.all()

    elif (
        current_officer
        and current_officer.designation == Designation.INSPECTOR.value
    ):
        officers = (
            officers_query.filter(
                Officer.station == current_officer.station
            ).all()
        )

    else:
        officers = (
            officers_query.filter(
                Officer.id == current_officer.id
            ).all()
        )

    workloads = []

    for officer in officers:

        total_cases = (
            db.query(func.count(Case.id))
            .filter(
                Case.officer_id == officer.id
            )
            .scalar()
        )

        open_cases = (
            db.query(func.count(Case.id))
            .filter(
                Case.officer_id == officer.id,
                Case.status == CaseStatus.OPEN.value,
            )
            .scalar()
        )

        under_investigation_cases = (
            db.query(func.count(Case.id))
            .filter(
                Case.officer_id == officer.id,
                Case.status == CaseStatus.UNDER_INVESTIGATION.value,
            )
            .scalar()
        )

        closed_cases = (
            db.query(func.count(Case.id))
            .filter(
                Case.officer_id == officer.id,
                Case.status == CaseStatus.CLOSED.value,
            )
            .scalar()
        )

        workloads.append(
            OfficerWorkloadResponse(
                officer_id=officer.id,
                badge_number=officer.badge_number,
                name=officer.name,
                designation=officer.designation,
                station=officer.station,
                total_cases=total_cases,
                open_cases=open_cases,
                under_investigation_cases=under_investigation_cases,
                closed_cases=closed_cases,
            )
        )

    return OfficerWorkloadsResponse(
        officers=workloads
    )
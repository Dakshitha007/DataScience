from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.case_assignment import CaseAssignment
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
    OfficerRank,
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

    return InvestigationDashboardResponse(
        total_cases=query.count(),
        open_cases=query.filter(
            Case.status == CaseStatus.OPEN
        ).count(),
        closed_cases=query.filter(
            Case.status == CaseStatus.CLOSED
        ).count(),
        under_investigation=query.filter(
            Case.status == CaseStatus.IN_PROGRESS
        ).count(),
        high_priority=query.filter(
            Case.priority == CasePriority.HIGH
        ).count(),
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
        query.order_by(
            Case.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return RecentCasesResponse(
        cases=[
            CaseSummaryResponse(
                id=case.id,
                case_number=case.case_number,
                fir_number=case.fir_number,
                crime_type=case.crime_type,
                title=case.title,
                status=case.status,
                priority=case.priority,
                police_station_id=case.police_station_id,
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
    fir_number: str | None = None,
    title: str | None = None,
    crime_type: str | None = None,
    status: CaseStatus | None = None,
    priority: CasePriority | None = None,
    police_station_id: int | None = None,
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

    if fir_number:
        query = query.filter(
            Case.fir_number.ilike(f"%{fir_number}%")
        )

    if title:
        query = query.filter(
            Case.title.ilike(f"%{title}%")
        )

    if crime_type:
        query = query.filter(
            Case.crime_type.ilike(f"%{crime_type}%")
        )

    if status:
        query = query.filter(
            Case.status == status
        )

    if priority:
        query = query.filter(
            Case.priority == priority
        )

    if police_station_id:
        query = query.filter(
            Case.police_station_id == police_station_id
        )

    cases = query.order_by(
        Case.created_at.desc()
    ).all()

    return SearchCasesResponse(
        cases=[
            CaseSummaryResponse(
                id=case.id,
                case_number=case.case_number,
                fir_number=case.fir_number,
                crime_type=case.crime_type,
                title=case.title,
                status=case.status,
                priority=case.priority,
                police_station_id=case.police_station_id,
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
                    CaseStatus.OPEN,
                    CaseStatus.IN_PROGRESS,
                ]
            )
        )
        .order_by(
            Case.created_at.desc()
        )
        .all()
    )

    return PendingCasesResponse(
        cases=[
            CaseSummaryResponse(
                id=case.id,
                case_number=case.case_number,
                fir_number=case.fir_number,
                crime_type=case.crime_type,
                title=case.title,
                status=case.status,
                priority=case.priority,
                police_station_id=case.police_station_id,
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
            Case.status == CaseStatus.OPEN
        ).count(),
        closed_cases=query.filter(
            Case.status == CaseStatus.CLOSED
        ).count(),
        under_investigation=query.filter(
            Case.status == CaseStatus.IN_PROGRESS
        ).count(),
        high_priority=query.filter(
            Case.priority == CasePriority.HIGH
        ).count(),
        medium_priority=query.filter(
            Case.priority == CasePriority.MEDIUM
        ).count(),
        low_priority=query.filter(
            Case.priority == CasePriority.LOW
        ).count(),
    )
def get_case_details(
    db: Session,
    case_id: int,
    current_user: User,
    current_officer: Officer | None,
):
    case = authorize_case_access(
        db,
        case_id,
        current_user,
        current_officer,
    )

    officers = []

    for assignment in case.case_assignments:
        officer = assignment.officer

        if officer is None:
            continue

        officers.append(
            OfficerInfoResponse(
                id=officer.id,
                badge_number=officer.badge_number,
                first_name=officer.first_name,
                last_name=officer.last_name,
                rank=officer.rank,
                phone=officer.phone,
            )
        )

    return CaseDetailsResponse(
        id=case.id,
        case_number=case.case_number,
        fir_number=case.fir_number,
        crime_type=case.crime_type,
        title=case.title,
        description=case.description,
        status=case.status,
        priority=case.priority,
        police_station_id=case.police_station_id,
        officers=officers,
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
        current_officer is not None
        and current_officer.rank == OfficerRank.INSPECTOR
    ):
        officers = (
            officers_query.filter(
                Officer.police_station_id == current_officer.police_station_id
            ).all()
        )

    else:
        if current_officer is None:
            officers = []
        else:
            officers = (
                officers_query.filter(
                    Officer.id == current_officer.id
                ).all()
            )

    workloads = []

    for officer in officers:

        assignments = (
            db.query(CaseAssignment)
            .filter(
                CaseAssignment.officer_id == officer.id
            )
            .all()
        )

        case_ids = [a.case_id for a in assignments]

        total_cases = 0
        open_cases = 0
        in_progress_cases = 0
        closed_cases = 0

        if case_ids:
            total_cases = (
                db.query(Case)
                .filter(Case.id.in_(case_ids))
                .count()
            )

            open_cases = (
                db.query(Case)
                .filter(
                    Case.id.in_(case_ids),
                    Case.status == CaseStatus.OPEN,
                )
                .count()
            )

            in_progress_cases = (
                db.query(Case)
                .filter(
                    Case.id.in_(case_ids),
                    Case.status == CaseStatus.IN_PROGRESS,
                )
                .count()
            )

            closed_cases = (
                db.query(Case)
                .filter(
                    Case.id.in_(case_ids),
                    Case.status == CaseStatus.CLOSED,
                )
                .count()
            )

        workloads.append(
            OfficerWorkloadResponse(
                officer_id=officer.id,
                badge_number=officer.badge_number,
                first_name=officer.first_name,
                last_name=officer.last_name,
                rank=officer.rank,
                total_cases=total_cases,
                open_cases=open_cases,
                under_investigation_cases=in_progress_cases,
                closed_cases=closed_cases,
            )
        )

    return OfficerWorkloadsResponse(
        officers=workloads
    )
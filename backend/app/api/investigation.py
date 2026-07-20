from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_officer,
    get_current_user,
)
from app.database.session import get_db

from app.models.officer import Officer
from app.models.user import User

from app.schemas.investigation import (
    CaseDetailsResponse,
    InvestigationDashboardResponse,
    InvestigationStatisticsResponse,
    OfficerWorkloadsResponse,
    PendingCasesResponse,
    RecentCasesResponse,
    SearchCasesResponse,
)

from app.services.investigation_service import (
    get_case_details,
    get_dashboard_summary,
    get_investigation_statistics,
    get_officer_workloads,
    get_pending_cases,
    get_recent_cases,
    search_cases,
)

router = APIRouter(
    prefix="/investigation",
    tags=["Investigation"],
)


@router.get(
    "/dashboard",
    response_model=InvestigationDashboardResponse,
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_dashboard_summary(
        db,
        current_user,
        current_officer,
    )


@router.get(
    "/recent-cases",
    response_model=RecentCasesResponse,
)
def recent_cases(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of recent cases to return",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_recent_cases(
        db,
        current_user,
        current_officer,
        limit,
    )


@router.get(
    "/pending-cases",
    response_model=PendingCasesResponse,
)
def pending_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_pending_cases(
        db,
        current_user,
        current_officer,
    )


@router.get(
    "/officer-workloads",
    response_model=OfficerWorkloadsResponse,
)
def officer_workloads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_officer_workloads(
        db,
        current_user,
        current_officer,
    )


@router.get(
    "/search",
    response_model=SearchCasesResponse,
)
def search(
    case_number: str | None = Query(default=None),
    title: str | None = Query(default=None),
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    station: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return search_cases(
        db=db,
        current_user=current_user,
        current_officer=current_officer,
        case_number=case_number,
        title=title,
        status=status,
        priority=priority,
        station=station,
    )


@router.get(
    "/statistics",
    response_model=InvestigationStatisticsResponse,
)
def statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_investigation_statistics(
        db,
        current_user,
        current_officer,
    )


@router.get(
    "/cases/{case_id}",
    response_model=CaseDetailsResponse,
)
def case_details(
    case_id: int = Path(
        ...,
        gt=0,
        description="Case ID",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_case_details(
        db=db,
        case_id=case_id,
        current_user=current_user,
        current_officer=current_officer,
    )
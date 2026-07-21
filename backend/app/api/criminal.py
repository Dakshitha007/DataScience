from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_officer,
    get_current_user,
)

from app.database.session import get_db

from app.models.officer import Officer
from app.models.user import User

from app.schemas.criminal import (
    CriminalCreate,
    CriminalListResponse,
    CriminalResponse,
    CriminalDashboardResponse,
    CriminalStatisticsResponse,
    CriminalUpdate,
)

from app.services.criminal_service import (
    create_criminal,
    delete_criminal,
    get_all_criminals,
    get_case_criminals,
    get_criminal_by_id,
    get_criminal_statistics,
    get_dashboard_summary,
    search_criminals,
    update_criminal,
)

router = APIRouter(
    prefix="/criminals",
    tags=["Criminals"],
)


@router.post(
    "/",
    response_model=CriminalResponse,
    status_code=201,
)
def create(
    criminal: CriminalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return create_criminal(
        db,
        criminal,
        current_user,
        current_officer,
    )


@router.get(
    "/",
    response_model=CriminalListResponse,
)
def get_all(
    db: Session = Depends(get_db),
):
    return get_all_criminals(db)


@router.get(
    "/search",
    response_model=CriminalListResponse,
)
def search(
    full_name: str | None = Query(None),
    alias: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return search_criminals(
        db,
        full_name,
        alias,
        status,
    )
@router.get(
    "/dashboard",
    response_model=CriminalDashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(db)


@router.get(
    "/statistics",
    response_model=CriminalStatisticsResponse,
)
def statistics(
    db: Session = Depends(get_db),
):
    return get_criminal_statistics(db)


@router.get(
    "/case/{case_id}",
    response_model=CriminalListResponse,
)
def case_criminals(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_case_criminals(
        db,
        case_id,
        current_user,
        current_officer,
    )


@router.get(
    "/{criminal_id}",
    response_model=CriminalResponse,
)
def get_by_id(
    criminal_id: int,
    db: Session = Depends(get_db),
):
    return get_criminal_by_id(
        db,
        criminal_id,
    )
@router.put(
    "/{criminal_id}",
    response_model=CriminalResponse,
)
def update(
    criminal_id: int,
    criminal: CriminalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return update_criminal(
        db,
        criminal_id,
        criminal,
        current_user,
        current_officer,
    )


@router.delete(
    "/{criminal_id}",
)
def delete(
    criminal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_criminal(
        db,
        criminal_id,
        current_user,
    )
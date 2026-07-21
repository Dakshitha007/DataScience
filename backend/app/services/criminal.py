from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.dependencies.auth import get_current_user
from app.dependencies.officer import get_current_officer

from app.models.officer import Officer
from app.models.user import User

from app.schemas.criminal import (
    CriminalCreate,
    CriminalDashboardResponse,
    CriminalListResponse,
    CriminalResponse,
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
):
    return create_criminal(
        db,
        criminal,
    )
@router.get(
    "/",
    response_model=CriminalListResponse,
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    return search_criminals(
        db=db,
        full_name=full_name,
        alias=alias,
        status=status,
    )
@router.get(
    "/dashboard",
    response_model=CriminalDashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_summary(db)
@router.get(
    "/statistics",
    response_model=CriminalStatisticsResponse,
)
def statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_criminal_statistics(db)
@router.get(
    "/{criminal_id}",
    response_model=CriminalResponse,
)
def get_one(
    criminal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
):
    return update_criminal(
        db,
        criminal_id,
        criminal,
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
    )
@router.get(
    "/case/{case_id}",
    response_model=CriminalListResponse,
)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_case_criminals(
        db=db,
        case_id=case_id,
        current_user=current_user,
        current_officer=current_officer,
    )

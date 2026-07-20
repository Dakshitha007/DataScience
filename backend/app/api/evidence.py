from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_officer,
    get_current_user,
)
from app.database.session import get_db

from app.models.officer import Officer
from app.models.user import User

from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceUpdate,
    EvidenceResponse,
    EvidenceListResponse,
    EvidenceDashboardResponse,
    EvidenceStatisticsResponse,
)

from app.services.evidence_service import (
    create_evidence,
    get_all_evidence,
    get_evidence_by_id,
    update_evidence,
    delete_evidence,
    get_case_evidence,
    search_evidence,
    get_dashboard_summary,
    get_evidence_statistics,
)

router = APIRouter(
    prefix="/evidence",
    tags=["Evidence"],
)


@router.post(
    "/",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    evidence: EvidenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return create_evidence(
        db=db,
        evidence=evidence,
        current_user=current_user,
        current_officer=current_officer,
    )


@router.get(
    "/",
    response_model=EvidenceListResponse,
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_all_evidence(
        db,
        current_user,
        current_officer,
    )


@router.get(
    "/dashboard",
    response_model=EvidenceDashboardResponse,
)
def dashboard(
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
    "/statistics",
    response_model=EvidenceStatisticsResponse,
)
def statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_evidence_statistics(
        db,
        current_user,
        current_officer,
    )


@router.get(
    "/search",
    response_model=EvidenceListResponse,
)
def search(
    title: str | None = Query(default=None),
    evidence_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return search_evidence(
        db=db,
        current_user=current_user,
        current_officer=current_officer,
        title=title,
        evidence_type=evidence_type,
        status=status,
    )


@router.get(
    "/case/{case_id}",
    response_model=EvidenceListResponse,
)
def case_evidence(
    case_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_case_evidence(
        db=db,
        case_id=case_id,
        current_user=current_user,
        current_officer=current_officer,
    )


@router.get(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def get_by_id(
    evidence_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return get_evidence_by_id(
        db=db,
        evidence_id=evidence_id,
        current_user=current_user,
        current_officer=current_officer,
    )


@router.put(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def update(
    evidence_id: int,
    evidence: EvidenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return update_evidence(
        db=db,
        evidence_id=evidence_id,
        evidence_update=evidence,
        current_user=current_user,
        current_officer=current_officer,
    )


@router.delete(
    "/{evidence_id}",
)
def delete(
    evidence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    return delete_evidence(
        db=db,
        evidence_id=evidence_id,
        current_user=current_user,
        current_officer=current_officer,
    )
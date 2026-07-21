from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.evidence import Evidence
from app.models.officer import Officer
from app.models.user import User

from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceDashboardResponse,
    EvidenceListResponse,
    EvidenceResponse,
    EvidenceStatisticsResponse,
    EvidenceSummaryResponse,
    EvidenceUpdate,
)

from app.services.case_service import (
    authorize_case_access,
    get_accessible_cases_query,
)

from app.utils.enums import (
    EvidenceStatus,
    EvidenceType,
)
def create_evidence(
    db: Session,
    evidence: EvidenceCreate,
    current_user: User,
    current_officer: Officer | None,
):
    authorize_case_access(
        db=db,
        case_id=evidence.case_id,
        current_user=current_user,
        current_officer=current_officer,
    )

    db_evidence = Evidence(
        case_id=evidence.case_id,
        title=evidence.title,
        description=evidence.description,
        evidence_type=evidence.evidence_type.value,
        location_found=evidence.location_found,
        collected_by=evidence.collected_by,
        collection_date=evidence.collection_date,
        storage_location=evidence.storage_location,
        status=evidence.status.value,
    )

    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)

    return db_evidence
def get_evidence_by_id(
    db: Session,
    evidence_id: int,
    current_user: User,
    current_officer: Officer | None,
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    authorize_case_access(
        db=db,
        case_id=evidence.case_id,
        current_user=current_user,
        current_officer=current_officer,
    )

    return evidence
def get_all_evidence(
    db: Session,
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

    evidence = (
        db.query(Evidence)
        .filter(
            Evidence.case_id.in_(accessible_cases)
        )
        .order_by(
            Evidence.created_at.desc()
        )
        .all()
    )

    return EvidenceListResponse(
        evidence=[
            EvidenceSummaryResponse.model_validate(item)
            for item in evidence
        ]
    )
def get_case_evidence(
    db: Session,
    case_id: int,
    current_user: User,
    current_officer: Officer | None,
):
    authorize_case_access(
        db=db,
        case_id=case_id,
        current_user=current_user,
        current_officer=current_officer,
    )

    evidence = (
        db.query(Evidence)
        .filter(
            Evidence.case_id == case_id
        )
        .order_by(
            Evidence.collection_date.desc()
        )
        .all()
    )

    return EvidenceListResponse(
        evidence=[
            EvidenceSummaryResponse.model_validate(item)
            for item in evidence
        ]
    )
def search_evidence(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
    title: str | None = None,
    evidence_type: EvidenceType | None = None,
    status: EvidenceStatus | None = None,
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

    query = (
        db.query(Evidence)
        .filter(
            Evidence.case_id.in_(accessible_cases)
        )
    )

    if title:
        query = query.filter(
            Evidence.title.ilike(f"%{title}%")
        )

    if evidence_type:
        query = query.filter(
            Evidence.evidence_type == evidence_type.value
        )

    if status:
        query = query.filter(
            Evidence.status == status.value
        )

    evidence = (
        query.order_by(
            Evidence.collection_date.desc()
        )
        .all()
    )

    return EvidenceListResponse(
        evidence=[
            EvidenceSummaryResponse.model_validate(item)
            for item in evidence
        ]
    )
def update_evidence(
    db: Session,
    evidence_id: int,
    evidence_update: EvidenceUpdate,
    current_user: User,
    current_officer: Officer | None,
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    authorize_case_access(
        db=db,
        case_id=evidence.case_id,
        current_user=current_user,
        current_officer=current_officer,
    )

    update_data = evidence_update.model_dump(
        exclude_unset=True
    )

    if "evidence_type" in update_data:
        update_data["evidence_type"] = (
            update_data["evidence_type"].value
        )

    if "status" in update_data:
        update_data["status"] = (
            update_data["status"].value
        )

    for key, value in update_data.items():
        setattr(evidence, key, value)

    db.commit()
    db.refresh(evidence)

    return evidence
def delete_evidence(
    db: Session,
    evidence_id: int,
    current_user: User,
    current_officer: Officer | None,
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    authorize_case_access(
        db=db,
        case_id=evidence.case_id,
        current_user=current_user,
        current_officer=current_officer,
    )

    db.delete(evidence)
    db.commit()

    return {
        "message": "Evidence deleted successfully"
    }
def get_dashboard_summary(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    accessible_case_ids = (
        get_accessible_cases_query(
            db,
            current_user,
            current_officer,
        )
        .with_entities(Case.id)
        .subquery()
    )

    query = (
        db.query(Evidence)
        .filter(
            Evidence.case_id.in_(accessible_case_ids)
        )
    )

    return EvidenceDashboardResponse(
        total_evidence=query.count(),

        collected=query.filter(
            Evidence.status == EvidenceStatus.COLLECTED.value
        ).count(),

        in_analysis=query.filter(
            Evidence.status == EvidenceStatus.IN_ANALYSIS.value
        ).count(),

        verified=query.filter(
            Evidence.status == EvidenceStatus.VERIFIED.value
        ).count(),

        archived=query.filter(
            Evidence.status == EvidenceStatus.ARCHIVED.value
        ).count(),
    )
def get_evidence_statistics(
    db: Session,
    current_user: User,
    current_officer: Officer | None,
):
    accessible_case_ids = (
        get_accessible_cases_query(
            db,
            current_user,
            current_officer,
        )
        .with_entities(Case.id)
        .subquery()
    )

    query = (
        db.query(Evidence)
        .filter(
            Evidence.case_id.in_(accessible_case_ids)
        )
    )

    return EvidenceStatisticsResponse(
        total_evidence=query.count(),

        photos=query.filter(
            Evidence.evidence_type == EvidenceType.PHOTO.value
        ).count(),

        videos=query.filter(
            Evidence.evidence_type == EvidenceType.VIDEO.value
        ).count(),

        documents=query.filter(
            Evidence.evidence_type == EvidenceType.DOCUMENT.value
        ).count(),

        audio=query.filter(
            Evidence.evidence_type == EvidenceType.AUDIO.value
        ).count(),

        weapons=query.filter(
            Evidence.evidence_type == EvidenceType.WEAPON.value
        ).count(),

        fingerprints=query.filter(
            Evidence.evidence_type == EvidenceType.FINGERPRINT.value
        ).count(),

        dna=query.filter(
            Evidence.evidence_type == EvidenceType.DNA.value
        ).count(),

        other=query.filter(
            Evidence.evidence_type == EvidenceType.OTHER.value
        ).count(),
    )
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import (
    EvidenceStatus,
    EvidenceType,
)


# -------------------------------------------------
# Create Evidence
# -------------------------------------------------

class EvidenceCreate(BaseModel):
    case_id: int
    title: str
    description: str | None = None

    evidence_type: EvidenceType

    location_found: str | None = None

    collected_by: str

    collection_date: datetime

    storage_location: str | None = None

    status: EvidenceStatus


# -------------------------------------------------
# Update Evidence
# -------------------------------------------------

class EvidenceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    evidence_type: EvidenceType | None = None

    location_found: str | None = None

    collected_by: str | None = None

    collection_date: datetime | None = None

    storage_location: str | None = None

    status: EvidenceStatus | None = None


# -------------------------------------------------
# Summary Response
# -------------------------------------------------

class EvidenceSummaryResponse(BaseModel):
    id: int
    title: str

    evidence_type: str

    status: str

    collection_date: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------------------------------
# Full Response
# -------------------------------------------------

class EvidenceResponse(BaseModel):
    id: int

    case_id: int

    title: str

    description: str | None

    evidence_type: str

    location_found: str | None

    collected_by: str

    collection_date: datetime

    storage_location: str | None

    status: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------------------------------
# List Response
# -------------------------------------------------

class EvidenceListResponse(BaseModel):
    evidence: list[EvidenceSummaryResponse]


# -------------------------------------------------
# Dashboard Response
# -------------------------------------------------

class EvidenceDashboardResponse(BaseModel):
    total_evidence: int

    collected: int

    in_analysis: int

    verified: int

    archived: int


# -------------------------------------------------
# Statistics Response
# -------------------------------------------------

class EvidenceStatisticsResponse(BaseModel):
    total_evidence: int

    photos: int
    videos: int
    documents: int
    audio: int
    weapons: int
    fingerprints: int
    dna: int
    other: int
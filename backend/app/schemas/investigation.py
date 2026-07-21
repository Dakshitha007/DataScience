from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import CasePriority, CaseStatus, OfficerRank


class InvestigationDashboardResponse(BaseModel):
    total_cases: int
    open_cases: int
    closed_cases: int
    under_investigation: int
    high_priority: int


class CaseSummaryResponse(BaseModel):
    id: int
    case_number: str
    fir_number: str
    crime_type: str
    title: str
    status: CaseStatus
    priority: CasePriority
    police_station_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecentCasesResponse(BaseModel):
    cases: list[CaseSummaryResponse]


class SearchCasesResponse(BaseModel):
    cases: list[CaseSummaryResponse]


class PendingCasesResponse(BaseModel):
    cases: list[CaseSummaryResponse]


class InvestigationStatisticsResponse(BaseModel):
    total_cases: int
    open_cases: int
    closed_cases: int
    under_investigation: int
    high_priority: int
    medium_priority: int
    low_priority: int


class OfficerInfoResponse(BaseModel):
    id: int
    badge_number: str
    first_name: str
    last_name: str
    rank: OfficerRank
    phone: str

    model_config = ConfigDict(from_attributes=True)


class CaseDetailsResponse(BaseModel):
    id: int
    case_number: str
    fir_number: str
    crime_type: str
    title: str
    description: str
    status: CaseStatus
    priority: CasePriority
    police_station_id: int
    officers: list[OfficerInfoResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OfficerWorkloadResponse(BaseModel):
    officer_id: int
    badge_number: str
    first_name: str
    last_name: str
    rank: OfficerRank
    total_cases: int
    open_cases: int
    under_investigation_cases: int
    closed_cases: int


class OfficerWorkloadsResponse(BaseModel):
    officers: list[OfficerWorkloadResponse]
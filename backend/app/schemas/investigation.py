from datetime import datetime

from pydantic import BaseModel


class InvestigationDashboardResponse(BaseModel):
    total_cases: int
    open_cases: int
    closed_cases: int
    under_investigation: int
    high_priority: int


class CaseSummaryResponse(BaseModel):
    id: int
    case_number: str
    title: str
    status: str
    priority: str
    station: str
    created_at: datetime


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
    name: str
    designation: str
    station: str


class CaseDetailsResponse(BaseModel):
    id: int
    case_number: str
    title: str
    description: str

    status: str
    priority: str
    station: str

    officer: OfficerInfoResponse

    created_at: datetime
    updated_at: datetime
class OfficerWorkloadResponse(BaseModel):
    officer_id: int
    badge_number: str
    name: str
    designation: str
    station: str

    total_cases: int
    open_cases: int
    under_investigation_cases: int
    closed_cases: int


class OfficerWorkloadsResponse(BaseModel):
    officers: list[OfficerWorkloadResponse]
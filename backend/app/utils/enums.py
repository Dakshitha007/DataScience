from enum import Enum


class AppRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class Designation(str, Enum):
    INSPECTOR = "Inspector"
    SUB_INSPECTOR = "Sub-Inspector"


class CaseStatus(str, Enum):
    OPEN = "Open"
    UNDER_INVESTIGATION = "Under Investigation"
    CLOSED = "Closed"


class CasePriority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
class EvidenceType(str, Enum):
    PHOTO = "Photo"
    VIDEO = "Video"
    DOCUMENT = "Document"
    AUDIO = "Audio"
    WEAPON = "Weapon"
    FINGERPRINT = "Fingerprint"
    DNA = "DNA"
    OTHER = "Other"


class EvidenceStatus(str, Enum):
    COLLECTED = "Collected"
    IN_ANALYSIS = "In Analysis"
    VERIFIED = "Verified"
    ARCHIVED = "Archived"
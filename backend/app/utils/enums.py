from enum import Enum


class AppRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


# ------------------------
# Officer
# ------------------------

class OfficerRank(str, Enum):
    CONSTABLE = "Constable"
    HEAD_CONSTABLE = "Head Constable"
    SUB_INSPECTOR = "Sub Inspector"
    INSPECTOR = "Inspector"
    DSP = "DSP"
    SP = "SP"
    ACP = "ACP"
    DCP = "DCP"
    DIG = "DIG"
    IG = "IG"
    ADGP = "ADGP"
    DGP = "DGP"


class OfficerStatus(str, Enum):
    ACTIVE = "Active"
    ON_LEAVE = "On Leave"
    SUSPENDED = "Suspended"
    RETIRED = "Retired"
    TRANSFERRED = "Transferred"


# ------------------------
# Case
# ------------------------

class CaseStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"

class CasePriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# ------------------------
# Criminal
# ------------------------

class CriminalStatus(str, Enum):
    ACTIVE = "Active"
    ARRESTED = "Arrested"
    WANTED = "Wanted"
    RELEASED = "Released"
    DECEASED = "Deceased"


class CriminalRelationType(str, Enum):
    GANG_MEMBER = "Gang Member"
    PARTNER = "Partner"
    FAMILY = "Family"
    SUPPLIER = "Supplier"
    FINANCIER = "Financier"
    ASSOCIATE = "Associate"
    UNKNOWN = "Unknown"


# ------------------------
# Evidence
# ------------------------

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

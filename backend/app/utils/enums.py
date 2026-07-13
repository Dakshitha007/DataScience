from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    OFFICER = "Officer"
    SUPERVISOR = "Supervisor"
from enum import Enum


class AppRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class Designation(str, Enum):
    INSPECTOR = "Inspector"
    SUB_INSPECTOR = "Sub-Inspector"
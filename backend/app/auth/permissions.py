from fastapi import HTTPException, status

from app.models.user import User
from app.models.officer import Officer

from app.utils.enums import AppRole, OfficerRank


def require_case_creation_permission(
    current_user: User,
    current_officer: Officer | None
):
    # Admin can create cases
    if current_user.role == AppRole.ADMIN:
        return

    # Inspector can create cases
    if (
        current_officer is not None
        and current_officer.rank == OfficerRank.INSPECTOR
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to create cases."
    )


def validate_case_update_permission(
    case_update,
    current_user: User,
    current_officer: Officer | None
):
    # Admin can update everything
    if current_user.role == AppRole.ADMIN:
        return

    update_data = case_update.model_dump(exclude_unset=True)

    # Inspector cannot change police station
    if (
        current_officer is not None
        and current_officer.rank == OfficerRank.INSPECTOR
    ):
        if "police_station_id" in update_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inspector cannot change police station."
            )
        return

    # Sub Inspector can update only status and description
    if (
        current_officer is not None
        and current_officer.rank == OfficerRank.SUB_INSPECTOR
    ):
        allowed_fields = {
            "status",
            "description"
        }

        invalid_fields = set(update_data.keys()) - allowed_fields

        if invalid_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Sub-Inspector cannot update: {', '.join(invalid_fields)}"
            )

        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to update this case."
    )


def require_case_delete_permission(
    current_user: User
):
    # Only Admin can delete cases
    if current_user.role == AppRole.ADMIN:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only Admin can delete cases."
    )
def filter_accessible_officers(
    officers: list[Officer],
    current_user: User,
    current_officer: Officer | None,
):
    # Admin → All officers
    if current_user.role == AppRole.ADMIN:
        return officers

    if current_officer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Officer access required.",
        )

    # Inspector → Same station
    if current_officer.rank == OfficerRank.INSPECTOR:
        return [
            officer
            for officer in officers
            if officer.police_station_id
            == current_officer.police_station_id
        ]

    # Other officers → Only own profile
    return [
        officer
        for officer in officers
        if officer.id == current_officer.id
    ]


def validate_officer_access(
    target_officer: Officer,
    current_user: User,
    current_officer: Officer | None,
):
    # Admin
    if current_user.role == AppRole.ADMIN:
        return

    if current_officer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Officer access required.",
        )

    # Inspector
    if current_officer.rank == OfficerRank.INSPECTOR:
        if (
            target_officer.police_station_id
            != current_officer.police_station_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access officers from another station.",
            )
        return

    # Other officers
    if target_officer.id != current_officer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own profile.",
        )
def require_criminal_create_permission(
    current_user: User,
    current_officer: Officer | None,
):
    # Admin can create
    if current_user.role == AppRole.ADMIN:
        return

    # Inspector can create
    if (
        current_officer is not None
        and current_officer.rank == OfficerRank.INSPECTOR
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to create criminal records.",
    )


def require_criminal_update_permission(
    current_user: User,
    current_officer: Officer | None,
):
    # Admin can update
    if current_user.role == AppRole.ADMIN:
        return

    # Inspector can update
    if (
        current_officer is not None
        and current_officer.rank == OfficerRank.INSPECTOR
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to update criminal records.",
    )


def require_criminal_delete_permission(
    current_user: User,
):
    # Only Admin can delete
    if current_user.role == AppRole.ADMIN:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only Admin can delete criminal records.",
    )
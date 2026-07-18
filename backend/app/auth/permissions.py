from fastapi import HTTPException, status

from app.models.user import User
from app.models.officer import Officer

from app.utils.enums import AppRole, Designation


def require_case_creation_permission(
    current_user: User,
    current_officer: Officer | None
):
    # Admin can create cases
    if current_user.role == AppRole.ADMIN.value:
        return

    # Inspector can create cases
    if (
        current_officer is not None
        and current_officer.designation == Designation.INSPECTOR.value
    ):
        return

    # Everyone else is denied
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to create cases."
    )


def validate_case_update_permission(
    case_update,
    current_user: User,
    current_officer: Officer | None
):
    # Admin -> Can update everything
    if current_user.role == AppRole.ADMIN.value:
        return

    update_data = case_update.model_dump(
        exclude_unset=True
    )

    # Inspector -> Cannot change station
    if (
        current_officer is not None
        and current_officer.designation == Designation.INSPECTOR.value
    ):
        if "station" in update_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inspector cannot change station."
            )

        return

    # Sub Inspector -> Can update only status & description
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


def require_case_delete_permission(
    current_user: User
):
    # Only Admin can delete cases
    if current_user.role == AppRole.ADMIN.value:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only Admin can delete cases."
    )
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.auth.permissions import (
    require_case_creation_permission,
    validate_case_update_permission,
    require_case_delete_permission,
)

from app.auth.dependencies import (
    get_current_user,
    get_current_officer,
)

from app.schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
)

from app.services.case_service import (
    get_accessible_cases,
    authorize_case_access,
    validate_officer_assignment,
    create_case,
    update_case,
    delete_case,
)

from app.models.user import User
from app.models.officer import Officer

router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


@router.get(
    "/",
    response_model=list[CaseResponse]
)
def read_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer)
):
    return get_accessible_cases(
        db,
        current_user,
        current_officer
    )


@router.get(
    "/{case_id}",
    response_model=CaseResponse
)
def read_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer)
):
    return authorize_case_access(
        db,
        case_id,
        current_user,
        current_officer
    )


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_case(
    case: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer)
):
    # Role Permission
    require_case_creation_permission(
        current_user,
        current_officer
    )

    # Officer Validation
    validate_officer_assignment(
        db,
        case.officer_id,
        current_user,
        current_officer
    )

    return create_case(
        db,
        case
    )


@router.put(
    "/{case_id}",
    response_model=CaseResponse
)
def update_existing_case(
    case_id: int,
    case_update: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer)
):
    # Resource-Level Authorization
    authorize_case_access(
        db,
        case_id,
        current_user,
        current_officer
    )

    # Field-Level Authorization
    validate_case_update_permission(
        case_update,
        current_user,
        current_officer
    )

    updated_case = update_case(
        db,
        case_id,
        case_update
    )

    return updated_case


@router.delete(
    "/{case_id}"
)
def delete_existing_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer)
):
    # Resource-Level Authorization
    authorize_case_access(
        db,
        case_id,
        current_user,
        current_officer
    )

    # Delete Permission
    require_case_delete_permission(
        current_user
    )

    delete_case(
        db,
        case_id
    )

    return {
        "message": "Case deleted successfully"
    }
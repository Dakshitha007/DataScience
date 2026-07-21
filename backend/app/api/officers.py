from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    require_admin,
    get_current_user,
    get_current_officer,
)
from app.auth.permissions import (
    filter_accessible_officers,
    validate_officer_access,
)
from app.database.session import get_db
from app.models.officer import Officer
from app.models.user import User
from app.schemas.officer import (
    OfficerCreate,
    OfficerUpdate,
    OfficerResponse,
)
from app.services.officer_service import (
    create_officer,
    delete_officer,
    get_all_officers,
    get_officer,
    get_officer_by_badge,
    get_officer_by_user_id,
    update_officer,
)

router = APIRouter(
    prefix="/officers",
    tags=["Officers"],
)


@router.post(
    "/",
    response_model=OfficerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_officer(
    officer: OfficerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    # Check whether the user exists
    user = db.query(User).filter(User.id == officer.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if badge number already exists
    existing_badge = get_officer_by_badge(
        db,
        officer.badge_number,
    )

    if existing_badge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Badge number already exists",
        )

    # Check if user already has an officer profile
    existing_officer = get_officer_by_user_id(
        db,
        officer.user_id,
    )

    if existing_officer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Officer profile already exists for this user",
        )

    return create_officer(
        db,
        officer,
    )


@router.get(
    "/",
    response_model=list[OfficerResponse],
)
def get_officers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    officers = get_all_officers(db)

    return filter_accessible_officers(
        officers,
        current_user,
        current_officer,
    )


@router.get(
    "/{officer_id}",
    response_model=OfficerResponse,
)
def get_officer_details(
    officer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_officer: Officer | None = Depends(get_current_officer),
):
    officer = get_officer(
        db,
        officer_id,
    )

    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found",
        )

    validate_officer_access(
        officer,
        current_user,
        current_officer,
    )

    return officer


@router.put(
    "/{officer_id}",
    response_model=OfficerResponse,
)
def update_existing_officer(
    officer_id: int,
    officer_update: OfficerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    officer = get_officer(
        db,
        officer_id,
    )

    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found",
        )

    # Check badge number uniqueness if updated
    if (
        officer_update.badge_number
        and officer_update.badge_number != officer.badge_number
    ):
        existing_badge = get_officer_by_badge(
            db,
            officer_update.badge_number,
        )

        if existing_badge:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Badge number already exists",
            )

    return update_officer(
        db,
        officer,
        officer_update,
    )


@router.delete(
    "/{officer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_officer(
    officer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    officer = get_officer(
        db,
        officer_id,
    )

    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found",
        )

    delete_officer(
        db,
        officer,
    )

    return None
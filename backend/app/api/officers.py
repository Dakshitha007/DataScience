from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database.session import get_db
from app.models.user import User
from app.schemas.officer import OfficerCreate, OfficerResponse
from app.services.officer_service import (
    create_officer,
    get_officer_by_badge,
    get_officer_by_user_id,
)

router = APIRouter(
    prefix="/officers",
    tags=["Officers"]
)


@router.post(
    "/",
    response_model=OfficerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_officer(
    officer: OfficerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Check whether the user exists
    user = db.query(User).filter(User.id == officer.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if badge number already exists
    existing_badge = get_officer_by_badge(
        db,
        officer.badge_number
    )

    if existing_badge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Badge number already exists"
        )

    # Check if this user already has an officer profile
    existing_officer = get_officer_by_user_id(
        db,
        officer.user_id
    )

    if existing_officer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Officer profile already exists for this user"
        )

    return create_officer(
        db,
        officer
    )
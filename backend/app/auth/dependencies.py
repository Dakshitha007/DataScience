from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.oauth2 import oauth2_scheme
from app.auth.jwt_handler import SECRET_KEY, ALGORITHM
from app.database.session import get_db

from app.models.user import User
from app.models.officer import Officer
from app.utils.enums import AppRole, Designation


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


def get_current_officer(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Admin users don't need an officer profile
    if current_user.role == AppRole.ADMIN.value:
        return None

    officer = (
        db.query(Officer)
        .filter(Officer.user_id == current_user.id)
        .first()
    )

    if officer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer profile not found"
        )

    return officer


def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != AppRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


def require_inspector(
    current_officer: Officer = Depends(get_current_officer)
):
    if current_officer.designation != Designation.INSPECTOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inspector access required"
        )

    return current_officer


def require_sub_inspector(
    current_officer: Officer = Depends(get_current_officer)
):
    if current_officer.designation != Designation.SUB_INSPECTOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sub-Inspector access required"
        )

    return current_officer
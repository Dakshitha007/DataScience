from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.hashing import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = User(
        email=user.email,
        password=hashed_password,
        role=user.role.value
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
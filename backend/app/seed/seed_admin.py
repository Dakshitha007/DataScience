from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.hashing import hash_password
from app.utils.enums import AppRole


def seed_admin(db: Session):
    existing_admin = (
        db.query(User)
        .filter(User.email == "admin@crimemind.ai")
        .first()
    )

    if existing_admin:
        print("✅ Admin already exists.")
        return

    admin = User(
        email="admin@crimemind.ai",
        password=hash_password("Admin@123"),
        role=AppRole.ADMIN.value
    )

    db.add(admin)
    db.commit()

    print("✅ Default admin created.")
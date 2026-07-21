from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class CaseAssignment(Base):
    __tablename__ = "case_assignments"

    __table_args__ = (
    UniqueConstraint(
        "case_id",
        "officer_id",
        name="uq_case_officer",
    ),
    )


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False
    )

    officer_id = Column(
        Integer,
        ForeignKey("officers.id", ondelete="CASCADE"),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False,
        default="Investigator"
    )

    assigned_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    assigned_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    remarks = Column(
    String(255),
    nullable=True
    )

    assigned_by_user = relationship(
    "User",
    foreign_keys=[assigned_by],
    )


    case = relationship(
        "Case",
        back_populates="case_assignments"
    )

    officer = relationship(
        "Officer",
        back_populates="case_assignments"
    )
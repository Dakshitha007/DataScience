from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class CaseCriminal(Base):
    __tablename__ = "case_criminals"

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

    criminal_id = Column(
        Integer,
        ForeignKey("criminals.id", ondelete="CASCADE"),
        nullable=False
    )

    role = Column(
        String(50),
        default="Suspect"
    )

    case = relationship(
        "Case",
        back_populates="criminals"
    )

    criminal = relationship(
        "Criminal",
        back_populates="cases"
    )
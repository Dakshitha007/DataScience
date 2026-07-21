from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class CriminalRelation(Base):
    __tablename__ = "criminal_relations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    criminal_id = Column(
        Integer,
        ForeignKey("criminals.id", ondelete="CASCADE"),
        nullable=False
    )

    related_criminal_id = Column(
        Integer,
        ForeignKey("criminals.id", ondelete="CASCADE"),
        nullable=False
    )

    relation_type = Column(
        String(50),
        nullable=False
    )

    strength = Column(
        Integer,
        default=1
    )

    criminal = relationship(
        "Criminal",
        foreign_keys=[criminal_id],
        back_populates="outgoing_relations"
    )

    related_criminal = relationship(
        "Criminal",
        foreign_keys=[related_criminal_id],
        back_populates="incoming_relations"
    )
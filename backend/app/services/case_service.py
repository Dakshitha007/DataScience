from sqlalchemy.orm import Session

from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate


def get_all_cases(db: Session):
    return db.query(Case).all()


def get_case_by_id(db: Session, case_id: int):
    return db.query(Case).filter(Case.id == case_id).first()


def create_case(db: Session, case: CaseCreate):
    db_case = Case(
        case_number=case.case_number,
        title=case.title,
        description=case.description,
        status=case.status,
        priority=case.priority,
        officer_id=case.officer_id
    )

    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    return db_case


def update_case(
    db: Session,
    case_id: int,
    case_update: CaseUpdate
):
    db_case = get_case_by_id(db, case_id)

    if not db_case:
        return None

    update_data = case_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_case, key, value)

    db.commit()
    db.refresh(db_case)

    return db_case


def delete_case(db: Session, case_id: int):
    db_case = get_case_by_id(db, case_id)

    if not db_case:
        return None

    db.delete(db_case)
    db.commit()

    return db_case
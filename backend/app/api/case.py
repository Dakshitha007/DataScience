from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
)
from app.services.case_service import (
    get_all_cases,
    get_case_by_id,
    create_case,
    update_case,
    delete_case,
)

router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


@router.get("/", response_model=list[CaseResponse])
def read_cases(db: Session = Depends(get_db)):
    return get_all_cases(db)


@router.get("/{case_id}", response_model=CaseResponse)
def read_case(case_id: int, db: Session = Depends(get_db)):
    case = get_case_by_id(db, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_case(
    case: CaseCreate,
    db: Session = Depends(get_db),
):
    return create_case(db, case)


@router.put("/{case_id}", response_model=CaseResponse)
def update_existing_case(
    case_id: int,
    case_update: CaseUpdate,
    db: Session = Depends(get_db),
):
    updated_case = update_case(
        db,
        case_id,
        case_update,
    )

    if updated_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return updated_case


@router.delete("/{case_id}")
def delete_existing_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    deleted_case = delete_case(db, case_id)

    if deleted_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return {
        "message": "Case deleted successfully"
    }
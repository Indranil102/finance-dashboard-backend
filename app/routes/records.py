from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app import models, schemas
from app.dependencies import get_db, require_role, get_current_user

router = APIRouter()


# CREATE RECORD (admin only)
@router.post("/records")
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    new_record = models.Record(
        **record.dict(),
        created_by=user["email"]
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


# GET RECORDS (analyst + admin)
@router.get("/records")
def get_records(
    category: Optional[str] = None,
    type: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(require_role("analyst"))
):
    query = db.query(models.Record).filter(
        models.Record.is_deleted == False
    )

    if category:
        query = query.filter(models.Record.category == category)

    if type:
        query = query.filter(models.Record.type == type)

    offset = (page - 1) * limit

    records = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "data": records
    }


# UPDATE RECORD (admin only)
@router.put("/records/{record_id}")
def update_record(
    record_id: int,
    updated_data: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    record = db.query(models.Record).filter(
        models.Record.id == record_id,
        models.Record.is_deleted == False
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in updated_data.dict().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


# SOFT DELETE RECORD (admin only)
@router.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    record = db.query(models.Record).filter(
        models.Record.id == record_id,
        models.Record.is_deleted == False
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.is_deleted = True
    db.commit()

    return {"message": "Record deleted successfully"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app import models, schemas
from app.dependencies import get_db, require_role

router = APIRouter()

@router.post("/records")
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role("admin"))
):
    new_record = models.Record(**record.dict())

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/records")
def get_records(
    category: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("analyst"))
):
    query = db.query(models.Record)

    if category:
        query = query.filter(models.Record.category == category)

    if type:
        query = query.filter(models.Record.type == type)

    return query.all()

@router.put("/records/{record_id}")
def update_record(
    record_id: int,
    updated_data: schemas.RecordCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role("admin"))
):
    record = db.query(models.Record).filter(
        models.Record.id == record_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in updated_data.dict().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record

@router.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_role("admin"))
):
    record = db.query(models.Record).filter(
        models.Record.id == record_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}
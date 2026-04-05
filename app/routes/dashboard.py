from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.dependencies import get_db, require_role
from app import models

router = APIRouter()

@router.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    user=Depends(require_role("analyst"))
):
    total_income = db.query(func.sum(models.Record.amount)).filter(
        models.Record.type == "income"
    ).scalar() or 0

    total_expense = db.query(func.sum(models.Record.amount)).filter(
        models.Record.type == "expense"
    ).scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }
    
@router.get("/dashboard/category-summary")
def category_summary(
    db: Session = Depends(get_db),
    user=Depends(require_role("analyst"))
):
    results = (
        db.query(
            models.Record.category,
            func.sum(models.Record.amount)
        )
        .group_by(models.Record.category)
        .all()
    )

    return {
        category: total
        for category, total in results
    }
    
@router.get("/dashboard/recent")
def recent_activity(
    db: Session = Depends(get_db),
    user=Depends(require_role("analyst"))
):
    return (
        db.query(models.Record)
        .order_by(models.Record.date.desc())
        .limit(5)
        .all()
    )
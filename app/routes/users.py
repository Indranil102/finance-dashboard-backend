from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import hash_password
from app import models, schemas
from app.auth import verify_password, create_access_token
from app.dependencies import get_db
router= APIRouter()

@router.post("/login")
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):
    
    db_user= db.query(models.User).filter(models.User.email==user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found ")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token=create_access_token(
        {"sub": db_user.email,"role": db_user.role}
    )
    
    return {"access_token": token, "token_type": "bearer"}



@router.post("/users")
def create_user(user:schemas.UserCreate, db: Session= Depends(get_db)):
    
    existing_user= db.query(models.User).filter(models.User.email==user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user= models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
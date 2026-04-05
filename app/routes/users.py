router= APIRouter()

@router.get("/login")
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):
    
    db_user= db.query(models.User).filter(models.User.email==user.email).first()
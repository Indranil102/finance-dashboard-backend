from app.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email=payload.get("sub")
        role=payload.get("role")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "role": role}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def require_role(required_role:str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"]!= required_role:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return role_checker
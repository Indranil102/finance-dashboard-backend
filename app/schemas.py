from pydantic import BaseModel,EmailStr


#it for user
class UserBase(BaseModel):
    name:str
    email:EmailStr
    role:str
    
class UserCreate(UserBase):
    password:str
    
class UserResponse(UserBase):
    id:int 
    is_active:bool  
    
    class Config:
        from_attributes=True
        

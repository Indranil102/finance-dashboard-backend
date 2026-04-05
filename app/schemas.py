from pydantic import BaseModel,EmailStr
from datetime import date
from typing import Optional
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
        


# Record schema 

class RecordBase(BaseModel):
    amount:float
    type:str
    category:str
    date:date
    note:Optional[str]= None
    
class RecordCreate(RecordBase):
    pass


class recordResponse(RecordBase):
    id:int
    created_by:int
    
    class Config:
        from_attributes=True
        
        
class LoginSchema(BaseModel):
    email:EmailStr
    password:str
from sqlalchemy import Column,Integer, String,Boolean, Float,Date,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    password=Column(String,nullable=False)
    role=Column(String,default="viewer")
    is_active=Column(Boolean,default=True)
    
    
class Record(Base):
    __tablename__="records"
    
    id=Column(Integer,primary_key=True,index=True)
    amount=Column(Float,nullable=False)
    type=Column(String,nullable=False)
    category=Column(String,nullable=False)
    date=Column(Date)
    note=Column(String)
    
    created_by=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User")
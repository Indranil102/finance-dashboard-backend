from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import users




Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(users.router)

@app.get("/")
def home():
    return {"message":"Finance Dashboards"}
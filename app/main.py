from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import users
from app.routes import records
from app.routes import dashboard
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(dashboard.router)
app.include_router(users.router)
app.include_router(records.router)

@app.get("/")
def home():
    return {"message":"Finance Dashboards"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
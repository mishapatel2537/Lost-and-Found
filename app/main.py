from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.models import user
from app.api.routes import auth

app = FastAPI(title="Lost and Found")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Lost and Found API is running"}
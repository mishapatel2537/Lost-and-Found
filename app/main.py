from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.models import user
from app.api.routes import auth
from app.api.routes import users
from app.api.routes import items

app = FastAPI(title="Lost and Found")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)  #Auth routes
app.include_router(users.router) #User routes
app.include_router(items.router) #Item routes

@app.get("/")
def root():
    return {"message": "Lost and Found API is running"}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.base import Base
from app.db.session import engine
from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import items
from app.middleware.org_context import org_context_middleware

app = FastAPI(title="Lost and Found")

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)  #Auth routes
app.include_router(users.router) #User routes
app.include_router(items.router) #Item routes

app.middleware("http")(org_context_middleware)

@app.get("/")
def root():
    return {"message": "Lost and Found API is running"}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.base import Base
from app.db.session import engine
from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import items
from app.api.v1 import claims
from app.api.v1 import invite
from app.api.v1 import organization
from app.middleware.org_context import org_context_middleware

app = FastAPI(title="Lost and Found")

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(claims.router)
app.include_router(invite.router)
app.include_router(organization.router)

app.middleware("http")(org_context_middleware)

@app.get("/")
def root():
    return {"message": "Lost and Found API is running"}

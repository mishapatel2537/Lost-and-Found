from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.db.init_db import init_db
from app.api.v1 import auth, users, items, claims, invite, organization, notifications, admin, search
from app.middleware.org_context import org_context_middleware

app = FastAPI(title="Lost and Found API")

# Middleware must be added BEFORE routers
app.middleware("http")(org_context_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

try:
    import os
    os.makedirs("static/uploads", exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    pass

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(claims.router)
app.include_router(invite.router)
app.include_router(organization.router)
app.include_router(notifications.router)
app.include_router(admin.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"message": "Lost and Found API is running"}

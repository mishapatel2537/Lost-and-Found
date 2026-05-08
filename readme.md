# 🔍 Lost & Found — *Because some things deserve to be found*

> A production-grade REST API for managing lost and found items across organizations — built with FastAPI, PostgreSQL, and a little bit of hope.

---

## 🧭 What is this?

Ever lost your wallet at college and had zero way to check if someone turned it in? Yeah. This fixes that.

**Lost & Found** is a multi-tenant backend platform where organizations (colleges, offices, events) can run their own lost-and-found system — with smart item matching, proof-based claim verification, real-time notifications, and full admin control.

No more "just check the front desk." No more sticky notes on bulletin boards.

---

## ✨ Features

| Module | What it does |
|---|---|
| 🔐 **Auth** | Register, login, JWT tokens, bcrypt password hashing |
| 🏢 **Organizations** | Multi-tenant system — each org is isolated, invite-only |
| 🎟️ **Invite Codes** | Join an org only with a valid, time-limited invite code |
| 📦 **Items** | Report lost or found items with images, category, location |
| 🔁 **Claims** | Request to claim an item — with optional proof requirement |
| 🤖 **Smart Matching** | Automatically scores lost↔found item similarity by name, category & location |
| 🔔 **Notifications** | In-app alerts when someone claims your item or a claim is accepted/rejected |
| 🔍 **Search & Filter** | Search by keyword, filter by category, location, type, status |
| 👑 **Admin Panel** | View/delete users and items across the entire organization |
| 🛡️ **Role System** | `user` and `admin` roles with protected endpoints |

---

## 🏗️ Tech Stack

```
FastAPI          →  API framework
PostgreSQL       →  Database
SQLAlchemy       →  ORM
Alembic          →  Database migrations
Pydantic         →  Request/response validation
python-jose      →  JWT tokens
passlib[bcrypt]  →  Password hashing
python-multipart →  File/image uploads
```

---

## 🗂️ Project Structure

```
lost_and_found/
│
├── app/
│   ├── main.py                  # App entry point
│   │
│   ├── api/v1/                  # All route handlers
│   │   ├── auth.py              # Register & login
│   │   ├── users.py             # User profile
│   │   ├── items.py             # Lost/found item CRUD
│   │   ├── claims.py            # Claim requests
│   │   ├── notifications.py     # User notifications
│   │   ├── organization.py      # Org management
│   │   ├── invite.py            # Invite code generation
│   │   ├── admin.py             # Admin controls
│   │   └── search.py            # Smart matching
│   │
│   ├── core/
│   │   ├── config.py            # Environment config
│   │   └── security.py          # JWT & password hashing
│   │
│   ├── db/
│   │   ├── base.py              # SQLAlchemy base + model imports
│   │   ├── session.py           # DB engine & session
|   |   └──init_dp.py 
│   │
│   ├── models/                  # Database tables
│   ├── schemas/                 # Pydantic request/response models
│   ├── services/                # Business logic layer
│   ├── middleware/              # Auth & org context middleware
│   └── utils/                  # File upload, invite helpers
│
├── alembic/                     # Migration files
├── static/uploads/              # Uploaded item images
├── .env                         # Environment variables
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone & install

```bash
git clone https://github.com/yourusername/lost-and-found.git
cd lost-and-found
pip install -r requirements.txt
```

### 2. Set up your `.env`

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/lostfound
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Run migrations

```bash
alembic upgrade head
```

### 4. Start the server

```bash
uvicorn app.main:app --reload
```

### 5. Explore the API

Open **http://localhost:8000/docs** — FastAPI gives you a full interactive Swagger UI out of the box.

---

## 🔄 How it works (the happy path)

```
1. Admin creates an Organization
        ↓
2. Admin generates an Invite Code
        ↓
3. Users register using the Invite Code
        ↓
4. User reports a Lost Item (with image, location, category)
        ↓
5. Another user found something → reports a Found Item
        ↓
6. Smart Matching scores similarity → suggests possible matches
        ↓
7. Owner sees the found item → submits a Claim (with proof if required)
        ↓
8. Finder accepts the claim → item status becomes "claimed"
        ↓
9. Both users get notified 🔔
```

---

## 🤖 Smart Matching — how the scoring works

When you ask for matches on an item, the system scores every opposite-type item in your organization:

| Signal | Points |
|---|---|
| Name contains each other | +40 |
| Same category | +30 |
| Location overlap | +30 |
| **Total possible** | **100** |

Items scoring **40+** are returned as potential matches, sorted by score. Simple, fast, no ML required — but the architecture supports swapping in NLP similarity later.

---

## 📬 API Overview

```
POST   /auth/register           → Create account (requires invite code)
POST   /auth/login              → Get JWT token

GET    /users/me                → Your profile

POST   /items/                  → Report a lost/found item
POST   /items/upload            → Report with image
GET    /items/                  → List items (search, filter, paginate)
GET    /items/{id}              → Single item
PATCH  /items/{id}/status       → Update item status

POST   /claims/                 → Claim an item
PATCH  /claims/{id}             → Accept or reject a claim
GET    /claims/item/{item_id}   → Claim history for an item

GET    /notifications/          → Your notifications
PATCH  /notifications/read-all  → Mark all as read

GET    /search/matches/{item_id} → Smart matches for an item

POST   /organizations/          → Create organization
GET    /organizations/my/settings → Your org's settings

POST   /invite/invite-codes     → Generate invite code

GET    /admin/users             → [Admin] All users
DELETE /admin/users/{id}        → [Admin] Remove user
GET    /admin/items             → [Admin] All items
DELETE /admin/items/{id}        → [Admin] Remove item
```

---

## 🛡️ Security

- Passwords hashed with **bcrypt**
- Authentication via **JWT Bearer tokens**
- Organization isolation — users can only see items within their org
- Role-based access — admin endpoints reject non-admin users with `403`
- Rate limiting middleware ready to configure
- Secrets stored in `.env`, never hardcoded

---

## 🗺️ Future Scope

- [ ] WebSocket real-time notifications
- [ ] Email notifications (SMTP)
- [ ] Image similarity matching (CV-based)
- [ ] Google Maps location tagging
- [ ] Redis caching for search
- [ ] Frontend (React)

---

## 👤 Author

Built by **MISHA** as a backend portfolio project.  
Focused on clean architecture, real-world features, and production-ready patterns.

> *"I built the backend for finding lost things. Ironically, I now know exactly where everything is."*

---

use it, learn from it, improve it.
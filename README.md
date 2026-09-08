# SIH 2026 — AI-Powered Landslide Monitoring Backend

**PS ID: 26001** | North Eastern Region (NER)  
**Team Member**: M3 — Backend + PostGIS Engineer

---

## 🎯 What This Is

The central FastAPI backend for the SIH 2026 Landslide Monitoring System.  
Connects: M1 ML Engine ↔ M2 Field App ↔ M4 GIS Dashboard ↔ M5 Alerts ↔ M6 DevOps

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI + Uvicorn |
| Database | PostgreSQL + PostGIS |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Auth | JWT + bcrypt |
| GIS | GeoAlchemy2 + Shapely |
| Storage | Cloudinary (media files) |

---

## 🚀 Quick Start (Phase 1)

### 1. Prerequisites
- Python 3.12+
- Git
- PostgreSQL 16+ with PostGIS (needed from Phase 2)

### 2. Clone & Setup

```powershell
# Navigate to backend folder
cd "d:\sih 2026\backend"

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```powershell
# Copy example env file
Copy-Item .env.example .env
# Edit .env with your actual values (DB password, secret key, etc.)
```

### 4. Run the Server

```powershell
# With virtual environment activated:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test

| URL | What it does |
|-----|-------------|
| http://localhost:8000/ | Root health check |
| http://localhost:8000/health | Health endpoint |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc UI |

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              ← FastAPI app, CORS, routers
│   ├── core/
│   │   ├── config.py        ← Settings from .env
│   │   ├── database.py      ← SQLAlchemy async engine
│   │   ├── security.py      ← Password hashing + JWT
│   │   └── dependencies.py  ← FastAPI dependency injection
│   ├── models/              ← SQLAlchemy ORM models (Phase 5)
│   ├── schemas/             ← Pydantic request/response schemas (Phase 7)
│   ├── routers/             ← API route handlers (Phase 8+)
│   ├── services/            ← Business logic (Phase 8+)
│   ├── repositories/        ← Database query layer (Phase 8+)
│   ├── utils/               ← Helpers & utilities
│   └── middleware/          ← Custom middleware
├── migrations/              ← Alembic migration files (Phase 6)
├── tests/                   ← pytest test suite (Phase 30)
├── .env                     ← Local secrets (NEVER commit)
├── .env.example             ← Template (safe to commit)
├── .gitignore
├── requirements.txt
├── Dockerfile               ← (Phase 32)
└── docker-compose.yml       ← (Phase 32)
```

---

## 🗺️ Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Project Setup & FastAPI | ✅ Done |
| 2 | PostgreSQL + PostGIS | ⏳ Next |
| 3 | Database Architecture | ⏳ |
| 4 | Spatial Database Design | ⏳ |
| 5 | SQLAlchemy Models | ⏳ |
| 6 | Alembic Migrations | ⏳ |
| ... | ... | ⏳ |

---

## 🔐 Environment Variables

See `.env.example` for all required variables.

**Critical**: Never commit `.env` to Git. It is in `.gitignore`.

---

## 🧪 Running Tests (Phase 30)

```powershell
pytest tests/ -v
```

---

## 🌐 API Documentation

Interactive docs available at `/docs` (Swagger UI) and `/redoc`.

---

## 👥 Team

| ID | Role |
|----|------|
| M1 | Data + ML |
| M2 | Mobile/Web Field Reporting |
| **M3** | **Backend + PostGIS (this repo)** |
| M4 | GIS Dashboard |
| M5 | Alerts + External Data |
| M6 | Verification + DevOps |

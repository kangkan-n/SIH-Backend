"""
app/main.py

What this file does:
    - Creates the FastAPI application instance
    - Configures CORS (so M2/M4 frontends can call our API)
    - Mounts all API routers
    - Provides the root GET / health endpoint

Why CORS matters:
    CORS (Cross-Origin Resource Sharing) is a browser security feature.
    When M4's dashboard (running on localhost:3000) calls our API
    (running on localhost:8000), the browser blocks it unless our 
    backend explicitly allows it. We configure which origins are allowed.

This is the entry point — uvicorn runs this file.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

settings = get_settings()


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown events)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs code at startup and shutdown.
    
    Startup: Log that the server is ready.
    Shutdown: Cleanly close DB connection pool.
    
    We will add database connection checks here in Phase 2.
    """
    # STARTUP
    print(f"\n{'='*60}")
    print(f"  {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"  Environment : {settings.ENVIRONMENT}")
    print(f"  Debug mode  : {settings.DEBUG}")
    print(f"  Docs        : http://127.0.0.1:8000/docs")
    print(f"{'='*60}\n")
    
    yield  # App runs here
    
    # SHUTDOWN
    print("\nShutting down gracefully...")


# ---------------------------------------------------------------------------
# FastAPI Application Instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## SIH 2026 — AI-Powered Landslide Monitoring Backend

**PS ID: 26001** | North Eastern Region (NER)

This is the M3 Backend built with:
- **FastAPI** — High-performance Python web framework
- **PostgreSQL + PostGIS** — Spatial database
- **SQLAlchemy 2.x** — Async ORM
- **JWT** — Authentication

### Core Capabilities
- 🗺️ GIS-enabled field reports with PostGIS geometry
- 🤖 ML risk prediction integration (M1)
- 📱 Mobile field reporting API (M2)
- 🗺️ GeoJSON APIs for dashboard (M4)
- 🚨 Alert management (M5)
- ✅ Officer verification & audit (M6)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------
# CORS must be added BEFORE any routes.
# It tells browsers: "Yes, requests from these origins are allowed."
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],     # Authorization, Content-Type, etc.
)


# ---------------------------------------------------------------------------
# Root Endpoint (Phase 1 Test)
# ---------------------------------------------------------------------------
@app.get(
    "/",
    tags=["Health"],
    summary="Root health check",
    response_description="Basic server info and status",
)
async def root():
    """
    **Root endpoint** — confirms the FastAPI server is running.
    
    This is the first thing to test after starting the server.
    Expected response:
    ```json
    {
        "status": "ok",
        "message": "SIH Landslide Backend is running",
        ...
    }
    ```
    """
    return {
        "status": "ok",
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "http://127.0.0.1:8000/docs",
        "team": "M3 — Backend + PostGIS",
        "project": "SIH 2026 | PS ID: 26001",
    }


# ---------------------------------------------------------------------------
# Health Check Endpoint (used in Phase 33 for deployment monitoring)
# ---------------------------------------------------------------------------
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
async def health_check():
    """
    Health check endpoint for deployment monitoring.
    Load balancers and Docker health checks call this endpoint.
    
    In Phase 2, we will also check database connectivity here.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# ---------------------------------------------------------------------------
# Future routers will be included here (Phases 8–25)
# ---------------------------------------------------------------------------
# Example (do NOT add yet):
# from app.routers import auth, reports, risk, alerts
# app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
# app.include_router(reports.router, prefix=settings.API_V1_PREFIX)

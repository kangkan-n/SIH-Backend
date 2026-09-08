"""
app/core/database.py

What this file does:
    - Creates the SQLAlchemy async database engine
    - Creates the session factory (AsyncSession)
    - Provides a dependency function to get a DB session per-request

Why async?
    FastAPI is async-first. Using async SQLAlchemy means database queries
    don't block the server while waiting for PostgreSQL to respond.
    This lets FastAPI handle many concurrent requests efficiently.

We will flesh out models and migrations in Phases 3–6.
For Phase 1, this file just establishes the connection pattern.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
# create_async_engine: the core connection pool to PostgreSQL.
# echo=True in DEBUG mode prints every SQL query to the console — useful
# for development, but turn it OFF in production (it's very verbose).
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,          # Log SQL queries when DEBUG=True
    pool_pre_ping=True,           # Test connections before using them
    pool_size=10,                 # Keep 10 connections warm
    max_overflow=20,              # Allow up to 20 extra in a burst
)

# ---------------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------------
# AsyncSessionLocal is a factory. Each time you call AsyncSessionLocal(),
# you get a fresh async database session for one request.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,       # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------------------------
# Base Model
# ---------------------------------------------------------------------------
# All SQLAlchemy models (User, FieldReport, etc.) will inherit from Base.
# This ties all models together so Alembic can detect them for migrations.
class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Dependency: get_db
# ---------------------------------------------------------------------------
async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a database session.

    Usage in any router:
        @router.get("/something")
        async def my_endpoint(db: AsyncSession = Depends(get_db)):
            result = await db.execute(...)

    The 'async with' pattern ensures:
      - The session is automatically committed on success
      - The session is automatically rolled back on any exception
      - The connection is returned to the pool when done
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

"""
app/core/dependencies.py

What this file does:
    - FastAPI "dependencies" are reusable pieces of logic injected into routes.
    - This file contains commonly re-used dependencies across the entire API.

For Phase 1, this is mostly a placeholder.
We will add get_current_user, require_role, etc. in Phase 8 (Authentication).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db


# Re-export get_db so routers can import from one place
__all__ = ["get_db"]

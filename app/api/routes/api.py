from fastapi import APIRouter

from app.api.routes import memos, users

router = APIRouter()
router.include_router(memos.router, tags=["memos"], prefix="/memos")
router.include_router(users.router, tags=["users"], prefix="/users")

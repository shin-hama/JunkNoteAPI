from fastapi import APIRouter

from app.api.routes import authentication, memos, users


router = APIRouter(prefix="/api")
router.include_router(
    authentication.router, tags=["authentication"], prefix="/users"
)
router.include_router(memos.router, tags=["memos"], prefix="/memos")
router.include_router(users.router, tags=["users"], prefix="/users")

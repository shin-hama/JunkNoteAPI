from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.routes import memos, users

router = APIRouter()
router.include_router(memos.router, tags=["memos"], prefix="/memos")
router.include_router(users.router, tags=["users"], prefix="/users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
async def read_items(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    return {"token": token}

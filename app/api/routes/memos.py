from fastapi import APIRouter, Body, Depends


router = APIRouter()


@router.get
async def get_memos_for_user():
    memos = get_memos()

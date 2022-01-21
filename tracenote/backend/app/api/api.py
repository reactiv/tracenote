from fastapi import APIRouter

from app.api.endpoints import login, twitter

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(twitter.router, prefix="/twitter", tags=["twitter"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
from fastapi import APIRouter
from src.api.controller.v1.endpoints.comparison import router

api_router = APIRouter()

api_router.include_router(router, prefix="/comparison", tags=["comparison"])
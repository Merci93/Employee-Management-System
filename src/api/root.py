"""API root module"""
from fastapi import APIRouter


router = APIRouter(tags=["Root"])


@router.get("/v1/root/")
def get_root():
    return {"message": "Hello!!! Root API running."}

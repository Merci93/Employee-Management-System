"""API root module"""
from fastapi import APIRouter


root_router = APIRouter(tags=["Root"])


@root_router.get("/v1/root/")
def get_root():
    return {"message": "Hello!!! Root API running."}

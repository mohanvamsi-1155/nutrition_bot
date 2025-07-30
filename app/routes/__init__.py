from fastapi import FastAPI
from app.routes.loader_routes import router as loader_router


def router_matrix(app: FastAPI):
    app.include_router(loader_router, tags=["Loader"])

from fastapi import FastAPI
from app.routes.loader_routes import router as loader_router
from app.routes.searcher_routes import router as searcher_router


def router_matrix(app: FastAPI):
    app.include_router(loader_router, tags=["Loader"])
    app.include_router(searcher_router, tags=["Searcher"])


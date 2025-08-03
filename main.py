from fastapi import FastAPI
from app.routes import router_matrix
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Nutrition Bot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router_matrix(app)
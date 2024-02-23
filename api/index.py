from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware

from api.routes.router import api_router

app = FastAPI(
    title="app",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=UJSONResponse,
)

origins = [
    "http://localhost:5173",
    "*",
    "https://nutritious.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins for demonstration purposes
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router=api_router, prefix="/api")


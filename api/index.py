from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from api.routes.router import api_router

app = FastAPI(
    title="app",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=UJSONResponse,
)

app.include_router(router=api_router, prefix="/api")


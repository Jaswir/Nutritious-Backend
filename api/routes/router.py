from fastapi.routing import APIRouter
from api.routes.nutrition.views import router as nutrition_router


api_router = APIRouter()

# routes
api_router.include_router(router=nutrition_router, prefix="/nutrition")
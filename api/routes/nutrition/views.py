from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.service.image import convert_file_to_base64
from api.service.main import get_ingredients_from_image

router = APIRouter()


class ImageData(BaseModel):
    image_base64: str
@router.post("/get_ingredients_from_image")
async def create_upload_file(file: UploadFile = File(...)):
    """
    Accepts a file upload and encodes the file to Base64.
    """
    try:
        base64_image = await convert_file_to_base64(file)
        ingredients = await get_ingredients_from_image(base64_image)

        return {"filename": ingredients}
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

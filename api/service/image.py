

import base64
from fastapi import  UploadFile



async def convert_file_to_base64(upload_file: UploadFile) -> str:
    """
    Reads the uploaded file and encodes its content to Base64.

    :param upload_file: The uploaded file object.
    :return: The Base64 encoded string of the file's content.
    """
    # Read the file's content into memory
    file_content = await upload_file.read()
    # Encode the file content to Base64
    base64_encoded_content = base64.b64encode(file_content).decode('utf-8')
    return base64_encoded_content


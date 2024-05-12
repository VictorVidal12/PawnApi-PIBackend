from fastapi import File, UploadFile
import uuid
from fastapi import HTTPException


async def upload_img(IMGDIR, file: UploadFile = File(...), ):
    if file.filename.endswith(".jpg") or file.filename.endswith(".png") or file.filename.endswith(".jpeg"):
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
    else:
        raise HTTPException(status_code=400,
                            detail="invalid filetype . Please, upload an img filetype (.jpg, .jpeg or .png)")

    with open(f"{IMGDIR}{file.filename}", "wb") as f:
        f.write(contents)
    return file.filename

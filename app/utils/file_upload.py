import os
from fastapi import UploadFile
from uuid import uuid4

UPLOAD_DIR = "static/uploads"


def save_file(file: UploadFile):

    # create folder if not exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # unique filename
    filename = f"{uuid4()}_{file.filename}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    # save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
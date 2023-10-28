
from fastapi import UploadFile
from api.schema import FileSchema
from pathlib import Path
import shutil

def save_upload_file(
    upload_file: UploadFile, destination: FileSchema
) -> Path:
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
        print ("File uploaded sucessfully")


def convert_document_to_dict(document):
    return {
        'page_content': document.page_content,
        'metadata': document.metadata
    }

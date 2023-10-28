
from pydantic import BaseModel, FilePath, Field
from fastapi import UploadFile, File
from pathlib import Path
from typing import *

class ChatSchema(BaseModel):
    user_query: str
    #file_path: Optional[UploadFile] = File(..., description="Description of file_path")
    doc_id: str = None


class SummarySchema(BaseModel):
    context_words: str = Field(None, description="context at which user want the summarization to be.")
    # file: UploadFile = File(...)
    #file_path: Optional[UploadFile] = File(..., description="Description of file_path")
    runtype: str = Field('raw_text', description="runtype can either be raw_text or file")
    text: Optional[str] = Field(None, description="Required if you're summarizing for a text")
    query_url: Optional[str] = Field(None, description="Required if you're summarizing for a webpage")


class FileSchema(BaseModel):
    file_path: FilePath


class ChatResponse(BaseModel):
    answer: str

class SummaryResponse(BaseModel):
    summarization: str
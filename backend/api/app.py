
from runner.summarizer import SummaryBot
from runner.chatbot import ChatBot
from rag_engine.model_initializer import RAGModel
from rag_engine.embeddings import EmbedChunks
from rag_engine.flusher import flush, bytes_to_giga_bytes
from api.schema import ChatSchema, SummarySchema, ChatResponse, SummaryResponse
from api.utils import save_upload_file, convert_document_to_dict

from fastapi import FastAPI, HTTPException, UploadFile, status, File, Form
from langchain.llms import HuggingFacePipeline
from pathlib import Path
from typing import *
import logging
import os
import torch
import uuid

### ===================== Initialize model and embeddings ====================
## ===========================================================================

model = RAGModel()
text_generation_pipeline = model()
embedding_query = EmbedChunks().embedding_query
rag_model =  HuggingFacePipeline(pipeline = text_generation_pipeline)
UPLOAD_DIR = os.path.join(os.getcwd(), "db/input")


### ===================== Initialize API =================================
## =======================================================================

app = FastAPI()

print ("Initializing API....")
@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"status": "RAG model is up! Endpoints are `/chat` and `/summarize`."}


@app.post("/upload_doc", status_code=status.HTTP_200_OK)
def upload_chat_document(file_path: UploadFile = File(...)):

    fname = Path(file_path.filename)
    doc_id = str(uuid.uuid4())
    destination = os.path.join(UPLOAD_DIR, doc_id+fname.suffix)

    save_upload_file(file_path, destination)
    ChatBot.upsert_user_document(destination, doc_id) # upsert document to pinecone

    data = {
        "type": "chat",
        "document_path": destination if destination else None,
        "chat_doc": doc_id + ".json" if doc_id else None,
        "reference_id": doc_id,
    }

    ChatBot.store_result(data) # store reference of data
    response = {
        "user_doc_id": doc_id
    }

    return response


@app.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chatbot(user_query: str, doc_id: str = None):
    
    for _ in range(2):
        try:
            response = ChatBot.chat(user_query, rag_model, embedding_query, doc_id) # send user query to backend
            response['source_documents'] = [convert_document_to_dict(doc) for doc in response['source_documents']],

            data = {
                "qeury": user_query,
                "answer": response["answer"],
                "system_response": response,
            }

            ChatBot.store_result_chatbot(data, doc_id) # save user db for future reference
            return {"answer": response["answer"]}

        except RuntimeError as error:
            print (f"Caught an OutOfMemoryError: {error}")
            flush(model, text_generation_pipeline) # if CudaOutofMemoryError, it flushes out the model and pipeline initialization, the reintialize.
            print (bytes_to_giga_bytes(torch.cuda.max_memory_allocated()))
        except Exception as reason:
            raise HTTPException(status_code=500, detail=str(reason))


@app.post("/summarize", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
def summary(
    file_path: UploadFile = File(None), context_words: str = None, runtype: str = 'raw_text',
    text: Optional[str] = None, query_url: Optional[str] = None):

    if runtype == "raw_text":
        for _ in range(2):
            try:
                
                contextual_summary = SummaryBot.summary(
                    rag_model, embedding_query, context_words,
                    text, query_url, runtype)

                data = {
                    "type": "contextual_summarization",
                    "on": runtype,
                    "context": context_words,
                    "text": text, "query_url": query_url,
                    "summarization": contextual_summary}
                
                SummaryBot.store_result(data)
                return {"summarization": contextual_summary}

            except RuntimeError as error:
                print (f"Caught an OutOfMemoryError: {error}")
                flush(model, text_generation_pipeline)
                bytes_to_giga_bytes(torch.cuda.max_memory_allocated())
            except Exception as reason:
                logging.error(f"str{reason}")
                raise HTTPException(status_code=500, detail=str(reason))

    elif runtype == "file":
        for _ in range(2):
            try:
                print (file_path)
                fname = Path(file_path.filename)
                destination = os.path.join(UPLOAD_DIR, fname)

                save_upload_file(file_path, destination)

                contextual_summary = SummaryBot.summary_document(
                    rag_model, embedding_query, context_words, file_path=destination
                )

                data = {
                    "type": "contextual_summarization",
                    "on": runtype,
                    "context": context_words,
                    "document_id": file_path.split(".")[0],
                    "text": input.text, "query_url": query_url,
                    "summarization": contextual_summary}

                SummaryBot.store_result(data)
                # implement to remove the file immediately
                return {"summarization": contextual_summary}

            except RuntimeError as error:
                print (f"Caught an OutOfMemoryError: {error}")
                flush(model, text_generation_pipeline)
                bytes_to_giga_bytes(torch.cuda.max_memory_allocated())
            except Exception as reason:
                raise HTTPException(status_code=500, detail=str(reason))

    else:
        raise HTTPException(status_code=400, detail="Invalid runtype")

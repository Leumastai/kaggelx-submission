
# from runner.summarizer import SummaryBot
# from runner.chatbot import ChatBot
# from rag_engine.model_initializer import RAGModel
# from rag_engine.embeddings import EmbedChunks
# from rag_engine.flusher import flush, bytes_to_giga_bytes
# from api.schema import ChatSchema, SummarySchema, ChatResponse, SummaryResponse, FileSchema

# from fastapi import FastAPI, HTTPException, UploadFile, status, File, Form
# from langchain.llms import HuggingFacePipeline
# from pathlib import Path
# from typing import *
# import logging
# import uuid
# import os
# import shutil
# import torch


# # export PYTHONPATH=/home/unicconai/Documents/sam's_lab/archive/delete/kagglex:$PYTHONPATH

# print ("Running____________________")
# model = RAGModel()
# text_generation_pipeline = model()
# embedding_query = EmbedChunks().embedding_query
# rag_model =  HuggingFacePipeline(pipeline = text_generation_pipeline)


# app = FastAPI()

# UPLOAD_DIR = os.path.join(os.getcwd(), "db/input")

# def save_upload_file(
#     upload_file: UploadFile, destination: FileSchema
# ) -> Path:
#     try:
#         with open(destination, "wb") as buffer:
#             shutil.copyfileobj(upload_file.file, buffer)
#     finally:
#         upload_file.file.close()
#         print ("File uploaded sucessfully")


# print ("API Loading ..................................")
# @app.get("/", status_code=status.HTTP_200_OK)
# def home():
#     return {"status": "RAG model is up! Endpoints are `/chat` and `/summarize`."}


# @app.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
# # def chatbot(input: ChatSchema, file_path: Optional[UploadFile] = None,):
# def chatbot(user_query: str, file_path: Optional[UploadFile] = File(None)):
    
#     for _ in range(2):
#         # try:
#             print (file_path)
#             if file_path:
#                 fname = Path(file_path.filename)
#                 # rename file here
#                 doc_id = str(uuid.uuid4())
#                 destination = os.path.join(UPLOAD_DIR, doc_id+fname.suffix)

#                 save_upload_file(file_path, destination)
#                 ChatBot.upsert_user_document(destination, doc_id) # upsert document to pinecone

#                 data = {
#                     "type": "chat",
#                     "document_id": destination.split(".")[0] if destination else None,
#                     "chat_doc": doc_id + ".json" if doc_id else None,
#                     "reference_id": doc_id,
#                     #"user_query": user_query,
#                 }
#                 ChatBot.store_result(data)

#             response = ChatBot.chat(user_query, rag_model, embedding_query, doc_id) # send user query to backend
            
#             data = {
#                 "qeury": user_query,
#                 "answer": response["answer"],
#                 "response": response,
#             }
#             ChatBot.store_result_chatbot(data) # save user db for future reference


#             return {"answer": response["answer"]}
#         # except RuntimeError as error:
#         #     print (f"Caught an OutOfMemoryError: {error}")
#         #     flush(model, text_generation_pipeline) # if CudaOutofMemoryError, it flushes out the model and pipeline initialization, the reintialize.
#         #     print (bytes_to_giga_bytes(torch.cuda.max_memory_allocated()))
#         # except Exception as reason:
#         #     raise HTTPException(status_code=500, detail=str(reason))


# @app.post("/summarize", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
# #def summary(input: SummarySchema, file_path: UploadFile = File(...)):
# def summary(
#     file_path: UploadFile = File(...), context_words: str = None, runtype: str = 'raw_text',
#     text: Optional[str] = None, query_url: Optional[str] = None):

#     # if input.runtype == "raw_text":
#     if runtype == "raw_text":
#         for _ in range(2):
#             # try:
#                 # contextual_summary = SummaryBot.summary(
#                 #     rag_model, embedding_query, input.context_words,
#                 #     input.text, input.query_url, input.runtype)

#                 contextual_summary = SummaryBot.summary(
#                     rag_model, embedding_query, context_words,
#                     text, query_url, runtype)
                
#                 # data = {
#                 #     "type": "contextual_summarization",
#                 #     "on": input.runtype,
#                 #     "context": input.context_words,
#                 #     "text": input.text, "query_url": input.query_url,
#                 #     "summarization": contextual_summary}

#                 data = {
#                     "type": "contextual_summarization",
#                     "on": runtype,
#                     "context": context_words,
#                     "text": text, "query_url": query_url,
#                     "summarization": contextual_summary}
                
#                 SummaryBot.store_result(data)
#                 return {"summarization": contextual_summary}

#             # except RuntimeError as error:
#             #     print (f"Caught an OutOfMemoryError: {error}")
#             #     flush(model, text_generation_pipeline)
#             #     bytes_to_giga_bytes(torch.cuda.max_memory_allocated())
#             # except Exception as reason:
#             #     logging.error(f"str{reason}")
#             #     raise HTTPException(status_code=500, detail=str(reason))


#     # elif input.runtype == "file":
#     elif runtype == "file":
#         for _ in range(2):
#             # try:
#                 print (file_path)
#                 fname = Path(file_path.filename)
#                 destination = os.path.join(UPLOAD_DIR, fname)

#                 save_upload_file(file_path, destination)

#                 # contextual_summary = SummaryBot.summary_document(
#                 #     rag_model, embedding_query, input.context_words, file_path=destination
#                 # )

#                 contextual_summary = SummaryBot.summary_document(
#                     rag_model, embedding_query, context_words, file_path=destination
#                 )

#                 # data = {
#                 #     "type": "contextual_summarization",
#                 #     "on": input.runtype,
#                 #     "context": input.context_words,
#                 #     "document_id": file_path.split(".")[0],
#                 #     "text": input.text, "query_url": input.query_url,
#                 #     "summarization": contextual_summary}

#                 data = {
#                     "type": "contextual_summarization",
#                     "on": runtype,
#                     "context": context_words,
#                     "document_id": file_path.split(".")[0],
#                     "text": input.text, "query_url": query_url,
#                     "summarization": contextual_summary}

#                 SummaryBot.store_result(data)
#                 return {"summarization": contextual_summary}

#             # except RuntimeError as error:
#             #     print (f"Caught an OutOfMemoryError: {error}")
#             #     flush(model, text_generation_pipeline)
#             #     bytes_to_giga_bytes(torch.cuda.max_memory_allocated())
#             # except Exception as reason:
#             #     raise HTTPException(status_code=500, detail=str(reason))

#     # else:
#     #     raise HTTPException(status_code=400, detail="Invalid runtype")
    
# if __name__ == "__main__":
#     # uvicorn.run("src.rag_engine.main:app", host="0.0.0.0", port=1450, reload=True)
#     from backend.rag_engine.agent import SummaryAgent
#     contextual_summary = SummaryBot.summary(
#         rag_model, embedding_query, "TurboTax,\n IRS,\n Direct File",
#         query_url="https://techcrunch.com/2023/10/17/irs-will-pilot-free-direct-tax-filing-in-2024/",)
#     print (contextual_summary)
#     # summ = SummaryAgent(rag_model, embedding_query)
#     # print(summ(
#     #     "TurboTax,\n IRS,\n Direct File",
#     #     "https://techcrunch.com/2023/10/17/irs-will-pilot-free-direct-tax-filing-in-2024/",
#     # ))


# # First stage: Build dependencies and copy cache
# # FROM python:3.10.2 AS cache

# # WORKDIR /backend

# # # Install system dependencies
# # RUN apt-get update && \
# #     apt-get install -y --no-install-recommends build-essential ffmpeg libsm6 libxext6 cmake && \
# #     apt-get clean

# # # Copy only the requirements file and install dependencies
# # COPY requirements.txt .
# # RUN pip install --no-cache-dir -r requirements.txt

# # # Copy the .cache folder (50GB) into the first stage
# # COPY ./.cache ./.cache

# # # Second stage: Create the final image
# # FROM python:3.10.2

# # ENV INSTALL_PATH /backend

# # WORKDIR $INSTALL_PATH

# # # Copy the .cache folder from the first stage
# # COPY --from=cache /backend/.cache ./.cache

# # # Copy your application code (excluding .cache folder due to .dockerignore)
# # COPY . .

# # # Set environment variables
# # ENV PYTHONPATH="${INSTALL_PATH}:${PYTHONPATH}"
# # ENV TRANSFORMERS_CACHE=./.cache/huggingface/hub
# # ENV HF_HOME=./.cache/huggingface

# # EXPOSE 5000

# # # Make your entrypoint script executable
# # RUN chmod +x entrypoint.sh

# # # Define the entrypoint
# # ENTRYPOINT [ "./entrypoint.sh" ]

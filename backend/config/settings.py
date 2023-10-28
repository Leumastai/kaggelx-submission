
from dotenv import load_dotenv
import os
#load_dotenv(os.path.join(os.getcwd(), "config/.env"))
load_dotenv("config/.env")

MONGO_PASSWORD= os.environ.get("MONGO_PASSWORD")
MONGO_USERNAME=os.environ.get("MONGO_USERNAME")
MONGO_CLUSTER=os.environ.get("MONGO_CLUSTER")
RAG_DB_NAME = os.environ.get("RAG_DB_NAME")
RAG_COLL_NAME = os.environ.get("RAG_COLL_NAME")

mongo_configs = {
    "MONGO_PASSWORD" : MONGO_PASSWORD,
    "MONGO_USERNAME" : MONGO_USERNAME,
    "MONGO_CLUSTER" : MONGO_CLUSTER,
    "RAG_DB_NAME" : RAG_DB_NAME,
    "RAG_COLL_NAME" : RAG_COLL_NAME,
}

print (mongo_configs)
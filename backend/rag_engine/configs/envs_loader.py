
from dotenv import load_dotenv
import os

root_dir = os.getcwd()

env_path = os.path.join(root_dir, "rag_engine/.env")
print (env_path)
load_dotenv(env_path)

HF_AUTH = os.environ.get('HF_AUTH')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')

credentials = {
    'HF_AUTH':HF_AUTH,
    'PINECONE_API_KEY':PINECONE_API_KEY,
    'PINECONE_ENVIRONMENT': PINECONE_ENVIRONMENT,
}

print (credentials)
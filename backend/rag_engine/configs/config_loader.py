
from utils.loaders import yml_loader
from torch import cuda
import os

root_dir = os.getcwd()

configs_path = os.path.join(root_dir, 'rag_engine/configs/model_configs.yml')
db_configs_path = os.path.join(root_dir, 'rag_engine/configs/pinecone_db.yml')
chunk_configs_path = os.path.join(root_dir, 'rag_engine/configs/chunk_configs.yml')

configuratons = yml_loader(configs_path)
db_configurations = yml_loader(db_configs_path)
chunk_configurations = yml_loader(chunk_configs_path)

model_configs = configuratons['model_configs']
embedding_configs = configuratons['embeddings_configs']
pinecone_configs = db_configurations['pinecone_configs']
chunk_configs = chunk_configurations['chunk_configs']

print (db_configurations)
# device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
device = 1
print (device)
print("\n\n\n")
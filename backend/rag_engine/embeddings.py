
from typing import *
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from rag_engine.configs.config_loader import device, embedding_configs



class EmbedChunks:

    """
    Embedding class for embedding both text and documents using the embeddings model
    """

    def __init__(self) -> None:
        
        self.embedding_model_id = embedding_configs['embedding_model_id'][1]
        self.embedding_model_dim = embedding_configs['embedding_model_dim'][1]
        self.embedding_batch_size = embedding_configs['embedding_batch_size']
        self.cache_folder = embedding_configs['cache_folder']

        self.embeddings_model = HuggingFaceEmbeddings(
            model_name = self.embedding_model_id,
            #cache_folder = self.cache_folder,
            model_kwargs = {'device': device},
            encode_kwargs = {'device': device, 'batch_size': self.embedding_batch_size}
        )

    @property
    def embedding_query(self,):
        return self.embeddings_model.embed_query

    def __call__(self, batch_docs: List[str]) -> List[float]:
        embeddings = self.embeddings_model.embed_documents(batch_docs)
        return embeddings

if __name__ == "__main__":
    inst = EmbedChunks()
    print (inst(["who am I, in the begining?"])[0])



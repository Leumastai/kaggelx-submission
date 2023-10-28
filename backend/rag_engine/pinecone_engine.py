

import os
import time
from typing import Any
import pinecone
from typing import *
from rag_engine.configs.envs_loader import credentials
from rag_engine.configs.config_loader import pinecone_configs


# PINECONE_API_KEY = credentials['PINECONE_API_KEY']
# PINECONE_ENVIRONMENT = credentials['PINECONE_ENVIRONMENT']

class PineconeDB:

    """
    ### PineconeDB Engine
    This class deals with everything related to pinecone connection, querying and closing. 

    ##### NOTE: Samu, a context manger should be used here as its a resources we trying to manage here. 
    Do it when you're chanced
    """

    def __init__(self) -> None:
        
        self.index_name = pinecone_configs['index_name']
        self.index_metric = pinecone_configs['index_metric']

        pinecone.init(
            api_key = credentials['PINECONE_API_KEY'],
            environment = credentials['PINECONE_ENVIRONMENT']
        )

        try:
            if self.index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name = self.index_name,
                    dimension= pinecone_configs['embedding_dim'],
                    metric = self.index_metric,
                )

                # wait for the index to finish initilization
                while not pinecone.describe_index(self.index_name).status['ready']:
                    time.sleep(1)

                print (pinecone.describe_index(self.index_name))
        except Exception as reason:
            print (reason)

    def init_index(self, ) -> Any:
        for _ in range(2):
            try:
                self.index = pinecone.Index(self.index_name)
                print (self.index.describe_index_stats())
                return self.index
            except Exception as reason:
                print (f"An Error Occured reasons due to {reason}")

    '''def connect_to_index(self,):
        
        self.index = pinecone.Index(self.index_name)
        print (self.index.describe_index_stats())

        index = pinecone.GRPCIndex(index_name)
        index.describe_index_stats()

        return self.index'''

        # self.index.upsert(
    

    def upsert_to_index(self, id: List[str], embeddings: List[Any], metadata: List[Dict], namespace: Optional[str] = None,) -> None:
        self.index = self.init_index()
        self.index.upsert(
            vectors = zip(id, embeddings, metadata), # append user id as document id to metadata
            namespace = namespace# namespace should correspond to the pdf file
        )
    
    def query_vectors(
        self, text: str, top_k: int = 3, embedding_model: Optional[Any] = None, 
        filters: Optional[Dict] = None, namespace: Optional[str] = None,):
        
        if embedding_model:
            vectors = embedding_model.embed_documents(text)
            results = self.index.query(
                namespace=namespace,
                vectors=vectors,
                top_k = top_k,
                filter=filters,
                include_values=False,
                include_metadata=True,
            )

            # filter={
            #     "genre": {"$eq": "documentary"},
            #     "year": 2019
            # },

            return results

    def fetch_from_id(self, id: str):
        return self.index.fetch(id)

    def delete_index(self,):
        pinecone.delete_index(self.index_name)


    # def query_vector_by_index(self, text: str, index: str,  top_k: int = 3, embedding_model: Optional[Any] = None, namespace: Optional[str] = None,):

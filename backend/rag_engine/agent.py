

### Two agents will be available,
## ChatAgent
## SummaryAgent

import json
from typing import *
from pathlib import Path
from rag_engine.chat import chatbot
from rag_engine.loaders import Loaders
from rag_engine.retrieval import Retriever
from rag_engine.pinecone_engine import PineconeDB
from rag_engine.contextual_summarization import summarization

## Initialize db
pineconedb = PineconeDB()

# Chat with your data
class ChatAgent:

    """
    Chat Agent for chatting with your data.
    Procedure:
        - user sends in a documents
        - document upserted to pinecone
        - document is retrieved from pinecone based on the retrieval mechanism selected
        - document is passed alongside user query to LLM
    
    Constructor:
        llm: Any = LLModel 
        embedding_query: Any = embedding instance of the selected embedding model
    """

    def __init__(self, llm, embedding_query,) -> None:
        
        self.llm = llm
        self.index = pineconedb.init_index()
        self.retriever = Retriever(self.index, embedding_query)
        self.search_type: Union[str, float] = 'mmr'
        assert self.search_type in ['mmr', 'similarity', 'similarity_score_threshold']

    # def _save_chat_history(user_id, chat_history):
    #     # search if user in db

    #     json.dumps(chat_history)



    def __call__(self, query, user_id, **kwargs: Any,) -> Any:

        # filter based on the doc id give to the document the user uploaded from start. 
        # This helps latency not to query on all the dataset in the VDB
        if user_id != None:
            filter = { # qeury based on the document doc_id saved when upserting
                "doc_id" : {"$eq": f"{user_id}"}}

            db_retriever = self.retriever.default_retriever(
                self.search_type, **{
                    "k": 5, "lambda_mult": 0.6,
                    "filter": filter,}
            )

        else:
            db_retriever = self.retriever.default_retriever(
                self.search_type, **{
                "k": 5, "lambda_mult": 0.6,}
            )

        chat_response, chat_history = chatbot(query, db_retriever, self.llm, **kwargs)

        return chat_response



class SummaryAgent:

    """
    Summary Agent for contextual summarization based on the users
    point fo veiw and keywords.

    Constructor:
        llm: Union[HuggingFacePipeline, Any] = LLModel 
        embedding_query: Any = embedding instance of the selected embedding model
    """

    def __init__(self, llm, embedding_query) -> None:
        self.llm = llm
        self.index = pineconedb.init_index()
        self.retriever = Retriever(self.index, embedding_query)

    def __call__(
        self, context_words: str, 
        query_url: str = None, run_type: str = "raw_text",
        text: str = None, file_path: Union[str, Path] = None) -> Any:

        assert run_type in ['raw_text', 'file',]

        # This is valid when you want to do contextual summarization for a document
        if run_type == 'file': 
            print ("Running File ................................")
            assert file_path != None

            # first, load documents
            query_docs = Loaders.pdf_loader(file_path)

            # second retrieve document using contextual retriever. No need to send to VDB as its a one time thing.
            #retrieved_query = self.retriever.contextual_retriever(query_docs, self.llm)

            # third, send to summarization method
            contextual_summarization = summarization(
                self.llm, query_docs, run_type, key_words=context_words)

            return contextual_summarization
        
        # This is valid when you want to do contextual summarization on a raw text or webpage.
        if query_url: 
            print ("Running Query URL ................................")
            query_docs = Loaders.html_loader_default(query_url)
        elif text: 
            print ("Running Text  ................................")
            query_docs = Loaders.string_text_loader(text)
        
        contextual_summarization = summarization(
            self.llm, query_docs, run_type, key_words=context_words)
        return contextual_summarization

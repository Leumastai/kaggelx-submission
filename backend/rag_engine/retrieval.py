
from typing import *
from langchain import HuggingFacePipeline
from langchain.vectorstores import Pinecone
from langchain.schema.retriever import Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor


class Retriever():

    """
    Retrival class
    This class contains diverse methods for retriving documents from pinecone VDB.
    """

    def __init__(self, index, embedding_query) -> None:
        
        self.index = index
        self.text_field = "content"
        self.embedding_query = embedding_query

        self.vectorstore = Pinecone(
            self.index, self.embedding_query, self.text_field,
        )

    def similarity_search(self, query: str, k: int = 10, filter: Dict[str, str] = None) -> List[str]:
        """
        Get top query based on the most similar to the query using `cosine` similarity
        Args:
            - query: str = text to query form db
            - k: int = no. of results to return. default at 10
            - filter: Dict[str, str] = arguments to filter on the metadata

        Returns:
            - retriever_rslt: list of similar result tot the query
        """

        retriever_rslt = self.vectorstore.similarity_search(
            query, k, filter,
        )

        return retriever_rslt

    def mmr_search(self, query: str, k: int = 5, docs_diversity: float = 0.6, filter: Dict[str, str] = None) -> List[Document]:
        ## Maximum Marginal Relevance

        """
        MMR tries to get result relevant to the query and also add diversity among the results.

        Args:
            - query: str = text to query form db
            - k: int = deafualt (5) no. of results to return
            - docs_diversity: float = the percentage of diversity on the result. default at 60
            - filter: Dict[str, str] = arguments to filter on the metadata
        
        Returns:
            - retriever_rslt: list of similar result tot the query
        """

        retriever_rslt = self.vectorstore.max_marginal_relevance_search(
            query, k, lambda_mult=docs_diversity, filter=filter, 
        )

        return retriever_rslt

    def contextual_retriever(self, query: str, llm: Union[HuggingFacePipeline, Any], k: int = 10, prompt: Optional[str] = None,) -> str:

        """
        Contextual Compression (CC) helps improve the quality of the retrieved document. 
        CC helps improvr results by removing irrelevant information in the text using llms

        # default search type is similarity
        Args:
            - query: str = text to query from db
            - llm: Union[HuggingFacePipeline, Any] = loaded llm model
            - prompt: Optional[str]: prompt template to pass into the llm for better guidiance

        Returns:
            - retriever_rslt: list of results
        """

        compressor = LLMChainExtractor.from_llm(llm, prompt)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=self.vectorstore.as_retriever(search_kwargs = {"k": k}),
        )

        retriever_rslt = compression_retriever.get_relevant_documents(query)
        return retriever_rslt


    def ccr_combine(
        self, query: str, 
        llm: Union[HuggingFacePipeline, Any], 
        search_type: str, k: int=5, prompt: Optional[str] = None
        ) -> str:

        """
        Contextual Combine Retrieval combined with other retrieval method

        Args:
            - query: str = text to query form db
            - llm: Union[HuggingFacePipeline, Any] = loaded llm model
            - search_type:  str = type of search. either `mmr`, 
            - k: int = deafult (5). No. of search to return
            - prompt: Optional[str] = prompt template to pass into the llm for better guidiance

        Returns:
            - retriever_rslt: list of results
        """

        # docsearch.as_retriever(
        #     search_type="mmr",
        #     search_kwargs={'k': 6, 'lambda_mult': 0.25}
        # )

        assert search_type in ['mmr', 'similarity', 'similarity_score_threshold']
        
        compressor = LLMChainExtractor.from_llm(llm, prompt)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=self.vectorstore.as_retriever(search_type = search_type, search_kwargs = {"k": k}),
        )

        retriever_rslt = compression_retriever.get_relevant_documents(query)
        return retriever_rslt


    def self_query_search(self, metadata_info: List[Tuple], llm: Any, content_description: str, ):
        ## To infer metadata to the query itself.
        '''
        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="The lecture the chunk is from, should be one of `docs/cs229_lectures/MachineLearning-Lecture01.pdf`, `docs/cs229_lectures/MachineLearning-Lecture02.pdf`, or `docs/cs229_lectures/MachineLearning-Lecture03.pdf`",
                type="string",
            ),
            AttributeInfo(
                name="page",
                description="The page from the lecture",
                type="integer",
            ),
        ]
        '''
        retriever_rslt = SelfQueryRetriever.from_llm(
            llm, self.vectorstore, content_description, 
            metadata_info, verbose=True,
        )

        return retriever_rslt
    
    def default_retriever(self, search_type: str, **kwargs):

        """
        Default retriever when working with conversation chain directly from langchain.
        Args:
            - search_type: str = 'mmr', 'similarity', 'similarity_score_threshold'
            - kwargs
        """
        
        assert search_type in ['mmr', 'similarity', 'similarity_score_threshold']

        retriever_rslt = self.vectorstore.as_retriever(
            search_type=search_type, search_kwargs=kwargs
        )

        return retriever_rslt

    '''def __call__(self,) -> Any:
        self.vectorstore = Pinecone(
            self.index, self.embedding_query.embed_query, self.text_field,
        )'''

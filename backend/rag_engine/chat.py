
from typing import *
from langchain import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def chatbot(
    query: str, retriever: Any, 
    llm: Union[Any, HuggingFacePipeline], chain_type: str = 'stuff',
    chat_history: List[Tuple] = [],) -> str:

    """
    ### Conversation chat engine. 
    This function takes a couple of paramters and return a response to the user

    Args:
        - query: str = User query
        - llm: Union[Any, HuggingFacePipeline] = LLModel
        - chain_type: method to chain query response together to get one consolidated response. `stuff`, `map_reduce`
            default as `stuff`

    Returns:
        response: Dict[str]
    
    """

    ## Implement load chat history for the user here

    assert chain_type in ['stuff', 'map_reduce']

    ## Memory is now optional as it doesn't allow us to return_source_documents=True, 
    ## We manually save chat history and pass it in.

    # memory = ConversationBufferMemory(
    #     memory_key="chat_history",
    #     return_messages=True,
    # )
    
    # chat history should be a parameter, since we're passing it in and would like to save it
    

    #ConversationalRetrievalChain.from_scratch() # This how shitty bard is
    #retriever=vectordb.as_retriever(search_type=search_type, search_kwargs={'k': k})
    QA_CHAIN = ConversationalRetrievalChain.from_llm(
        llm,
        chain_type=chain_type,
        retriever=retriever,
        #memory=memory,
        return_source_documents=True,
        return_generated_question=True,
    )

    response = QA_CHAIN({"question": query, "chat_history": chat_history})
    chat_history.extend([(query, response['answer'])])
    return response, chat_history
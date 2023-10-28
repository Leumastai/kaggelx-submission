
##############################################################

# https://python.langchain.com/en/latest/modules/memory/examples/adding_memory_chain_multiple_inputs.html
template = """
- You are a chatbot named Botty having a conversation with a human.
- Your name is Botty.
- You have to be friendly.
- You are talking to a human.
- You NEVER answer that your are an AI language model.
- If you don't know the answer truthfully say you don't have an answer. Don't try to make up an answer.
- Always reply in the same language you are being asked.

Given the following extracted parts of a long document and a question, create a final answer.

{context}

{chat_history}
Human: {question}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "question", "context"], 
    template=template
)
session_id = 'UNIQUE FOR CLIENT SESSION OR SIMPLY CLIENT'
message_history = RedisChatMessageHistory(url=redisUrl, ttl=600, session_id=session_id)
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=message_history, input_key="question")
agent_chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)
search_index = FAISS.load_local(local_folder, OpenAIEmbeddings())
response = agent_chain(
    {
        "input_documents": search_index.similarity_search(query, k=1),
        "question": query,
    },
    return_only_outputs=True,
)

###################################################################################


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone
from templates.qa_prompt import QA_PROMPT
from templates.condense_prompt import CONDENSE_PROMPT

def query(openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index, pinecone_namespace):
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)

    pinecone.init(api_key=pinecone_api_key,environment=pinecone_environment)
    vectorstore = Pinecone.from_existing_index(index_name=pinecone_index, embedding=embeddings, text_key='text', namespace=pinecone_namespace)

    model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0, openai_api_key=openai_api_key)
    retriever = vectorstore.as_retriever(qa_template=QA_PROMPT, question_generator_template=CONDENSE_PROMPT)
    qa = ConversationalRetrievalChain.from_llm(llm=model, retriever=retriever, return_source_documents=True)

    return qa

########################################################################################

# Build prompt
from langchain.prompts import PromptTemplate
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

# Run chain
from langchain.chains import RetrievalQA
question = "Is probability a class topic?"
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vectordb.as_retriever(),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})


result = qa_chain({"query": question})
result["result"]

###################################################################################################


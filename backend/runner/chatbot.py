
from rag_engine.user_db_utils import UserDocument
from rag_engine.loaders import Loaders
from typing import Dict
import uuid

### ON: Work on DB for ChatBot and also saving user sessions 
# and user should be able to comeback and check their previous session
# STUDY, READ, AND FULLY UNDERSATND: the code ==> https://github.com/mobarski/ask-my-pdf/blob/main/srC
class ChatBot():

    __user_uuid__ = str(uuid.uuid4())

    @staticmethod
    def upsert_user_document(pdf_path, doc_id):

        chunked_docs = Loaders.pdf_loader(pdf_path)

        # user_db_instance = UserDocument(ChatBot.__user_uuid__)
        user_db_instance = UserDocument(doc_id)
        user_db_instance(chunked_docs)
    
    @staticmethod
    def chat(user_query, model, embedding_query, doc_id):

        from rag_engine.agent import ChatAgent
        chatbot_ = ChatAgent(model, embedding_query)
        # response = chatbot_(user_query, ChatBot.__user_uuid__)
        response = chatbot_(user_query, doc_id)
        print (response)
        print ("\n\n\n")

        return response

    @staticmethod
    def store_result(data: Dict[str, str]):
        # stores reference data to the chat history
        from runner.batch_send import add_data_to_file
        # data.update({"chat_id": ChatBot.__user_uuid__})
        # data.update({"chat_id": ChatBot.__user_uuid__})
        add_data_to_file(data)

    @staticmethod
    def store_result_chatbot(data: Dict[str, str], id: str = "unknown"):
        from runner.batch_send import add_data_to_file
        write_path = f"db/history/{id}"
        add_data_to_file(data, write_path)


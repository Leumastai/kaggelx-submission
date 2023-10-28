
import uuid

class SummaryBot():

    ## Immediatley afet user finishes uploading docs, this is what is loaded

    __user_id__ = str(uuid.uuid4())

    @staticmethod
    def summary(
        model, embedding_query, context_words: str, text: str = None,
        query_url: str = None, run_type: str = "raw_text",):

        from rag_engine.agent import SummaryAgent
        contextualbot = SummaryAgent(model, embedding_query,)
        
        if text:
            response = contextualbot(context_words, text=text, run_type=run_type)
            return response
        elif query_url:
            response = contextualbot(context_words, query_url=query_url, run_type=run_type)
            return response

    @staticmethod
    def summary_document(
        model, embedding_query, context_words: str, run_type: str = "file",
        file_path = None):

        from rag_engine.agent import SummaryAgent
        contextualbot = SummaryAgent(model, embedding_query,)
        response = contextualbot(
            context_words, run_type=run_type, file_path= file_path)

        return response

    @staticmethod
    def store_result(data):
        from runner.batch_send import add_data_to_file
        add_data_to_file(data)


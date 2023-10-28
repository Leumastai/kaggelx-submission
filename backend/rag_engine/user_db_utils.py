



# from src.rag_engine.pinecone_engine import PineconeDB
# from src.rag_engine.embeddings import EmbedChunks
# from langchain.schema.retriever import Document
# from typing import *
# import uuid


# class UserDB(PineconeDB):

#     def __init__(self) -> None:
#         super().__init__()
        
#         self.doc_id = str(uuid.uuid4())
#         self.chunk_batch_size = 32 # 64
#         self.embeddings_inst = EmbedChunks() # class composition or dependency injection


#     def __call__(self, chunks: List[Document], embeddings: Any) -> Any:

#         for i in range(0, len(chunks), self.chunk_batch_size):
            
#             batch_end = min(len(chunks), i+self.chunk_batch_size)
#             batch = chunks[i: batch_end]
            
#             batch_text: List[str] = [text.page_content for text in batch]
#             init_metadata = [text.metadata.update({
#                 "content": text.page_content,
#                 "doc_id": self.doc_id}) for text in batch]

#             batch_metadata = [text.metadata for text in batch]
#             uuid_strings = [str(uuid.uuid4()) for _ in range(len(batch))]

#             embeddings = self.embeddings_inst(batch_text)
#             self.upsert_to_index(uuid_strings, embeddings, batch_metadata,)

            
            #embeddings = embeddings_model.embed_documents(batch_text)
            # index.upsert(
            #     vectors = zip(uuid_strings, embeddings, batch_metadata),
            #     #namespace = pdf_uuid# namespace should correspond to the pdf file
            # )
    
from rag_engine.pinecone_engine import PineconeDB
from rag_engine.embeddings import EmbedChunks
from langchain.schema.retriever import Document
from typing import *
import uuid


class UserDocument(PineconeDB):

    """
    ### This class process a user document and upsert it to the VDB
    """
    def __init__(self, doc_id) -> None:
        """
        doc_id: str = A unique id for the user document to query whenever the user want to converse
        """
        super().__init__()
        self.doc_id = doc_id
        self.chunk_batch_size = 32 # 64
        self.embeddings_inst = EmbedChunks()
        # self.index = self.init_index()

    def _prepare_batch(self, chunks: List[Document]) -> Tuple[List[str], List[dict], List[str]]:
        batch_text = [text.page_content for text in chunks]
        batch_metadata = []
        uuid_strings = []

        for text in chunks:
            text.metadata.update({"content": text.page_content, "doc_id": self.doc_id})
            batch_metadata.append(text.metadata)
            uuid_strings.append(str(uuid.uuid4()))

        return batch_text, batch_metadata, uuid_strings

    def __call__(self, chunks: List[Document],) -> None:
        """
        chunks: List[Document] = A list of chunked document to send to the VDB
        """
        for i in range(0, len(chunks), self.chunk_batch_size):
            batch_end = min(len(chunks), i + self.chunk_batch_size)
            batch = chunks[i:batch_end]

            batch_text, batch_metadata, uuid_strings = self._prepare_batch(batch)
            batch_embeddings = self.embeddings_inst(batch_text)
            self.upsert_to_index(uuid_strings, batch_embeddings, batch_metadata)
        print ("Succefully upserted documents to Pinecone")


# class UserDB():

#     def load_user_db():

#     def save_user_db():


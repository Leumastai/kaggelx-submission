
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.schema.retriever import Document
from pathlib import Path
from typing import *


class Loaders:

    """
    A loader class for ease of loading documents 
    
    """

    @staticmethod
    def string_text_loader(text, chunk_size: int = 700, chunk_overlap: int = 100):
        from langchain.text_splitter import CharacterTextSplitter

        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
        return docs

    @staticmethod
    def html_loader_default(url, chunk_size: int = 700, chunk_overlap: int = 100):
        from rag_engine.commons import get_text_from_article_url
        from langchain.text_splitter import CharacterTextSplitter

        text = get_text_from_article_url(url)
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
        return docs

    @staticmethod
    def html_loader(url, chunk_size: int = 1000, chunk_overlap: int = 100):

        """
        Load documents from html url
        """

        from langchain.document_loaders import WebBaseLoader
        loader = WebBaseLoader(url)
        docs: List[Document] = loader.load()

        doc_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            length_function = len,
        )

        chunks = doc_splitter.split_documents(docs)
        return chunks

    @staticmethod
    def pdf_loader(pdf_path: Union[Path, str], chunk_size: int = 600, chunk_overlap: int = 80):

        """
        Load documents from pdf
        """

        from langchain.document_loaders import PyPDFLoader
        
        loader = PyPDFLoader(pdf_path)
        docs: List[Document] = loader.load()

        # set a threshold depending on the size of the documents for splitting
        # chunk_size = 350
        # chunk_overlap = 50

        doc_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            length_function = len,
        )

        chunks = doc_splitter.split_documents(docs)
        return chunks

#    """ @staticmethod
#     def video_loader(video_url):
#         # pip install yt_dlp
#         # pip install pydub
#         # pip install librosa

#         from langchain.document_loaders.generic import GenericLoader
#         from langchain.document_loaders.parsers import OpenAIWhisperParser, OpenAIWhisperParserLocal
#         from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader"""


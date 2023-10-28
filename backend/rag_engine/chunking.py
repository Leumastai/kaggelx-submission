

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from rag_engine.configs.config_loader import chunk_configs
from os import PathLike
from typing import *


class InputLoaders:
    def __init__(self, input_type: str, input_path: Union[PathLike, Any]) -> None:
        self.input_type = input_type
        self.input_path = input_path


class Chunkers:

    def __init__(self, input_type: str, input_path: Union[PathLike, Any]) -> None:
        self.input_type = input_type
        self.input_path = input_path

        self.doc_splitter = RecursiveCharacterTextSplitter(
                chunk_size = chunk_configs['chunk_size'],
                chunk_overlap = chunk_configs['chunk_overlap'],
                separators=["\n\n", "\n", " ", ""],
                length_function = len,
        )

    def __call__(self,):

        if self.input_type == 'pdf':

            from langchain.document_loaders import PyPDFLoader
            loaded_docs = PyPDFLoader(self.input_path).load()

            chunks = self.doc_splitter.split_documents(loaded_docs)
            return chunks

        if self.input_type == 'youtube':

            from langchain.document_loaders import YoutubeLoader
            loaded_docs = YoutubeLoader.from_youtube_url(self.input_path).load()

            chunks = self.doc_splitter.split_documents(loaded_docs)
            return chunks

        if self.input_type == 'html':

            from langchain.document_loaders import WebBaseLoader
            loaded_docs = WebBaseLoader(self.input_path).load()

            chunks = self.doc_splitter.split_documents(loaded_docs)
            return chunks





from langchain.document_loaders import PyPDFLoader
from os import PathLike
from typing import *

class InputLoaders:
    def __init__(self, input_type: str, input_path: Union[PathLike, Any]) -> None:
        self.input_type = input_type
        self.input_path = input_path

    def loaders(self,):

        if self.input_type == 'pdf':
            loader = PyPDFLoader(self.input_path)

            
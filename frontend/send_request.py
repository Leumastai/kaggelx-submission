
backend_api_url="http://api.backend:5000"
frontend_api_url="http://frontend.rag:8501"

import requests
from pathlib import Path
from typing import *


def upload_docs(file_path: Union[str, Path], url:str = 'http://localhost:5000/upload_doc'):
    # headers = {
    #     'accept': 'application/json',
    #     'Content-Type': 'multipart/form-data',}

    files = {
        'file_path': file_path}


    try:
        # response = requests.post(url, params=params, headers=headers)
        response = requests.post(url, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            return {"user_doc_id": f"Error: HTTP {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"user_doc_id": f"Request Error: {e}"}
    except Exception as e:
        return {"user_doc_id": f"Error occurred: {e}"}



    # headers = {
    #     'accept': 'application/json',
    #     # requests won't add a boundary if this header is set when you pass files=
    #     # 'Content-Type': 'multipart/form-data',
    # }

    # files = {
    #     'file_path': open('HowtoReadPaper.pdf;type=application/pdf', 'rb'),
    # }



def contextual_summarization(
    selection: str, context:str=None, file_path: Union[str, Path]=None, 
    text:str=None, webpage_url:str=None, url: str = 'http://localhost:5000/summarize'):

    import requests

    headers = {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data',
    } if file_path else {
        'accept': 'application/json',
    }

    if selection == "text":
        params = {
            'context_words': f'{context}',
            'runtype': 'raw_text',
            'text': f'{text}',
        }

        files = {
            'file_path': (None, ''),
        }
    
    elif selection == "url":
        params = {
            'context_words': f'{context}',
            'runtype': 'raw_text',
            'query_url': f'{webpage_url}',
        }

        files = {
            'file_path': (None, ''),
        }

    elif selection == "file":
        params = {
            'context_words': f'{context}',
            'runtype': 'file',
        }

        files = {
            'file_path': file_path,
        }

    try:
        response = requests.post(url, params=params, headers=headers, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            return {"summarization": f"Error: HTTP {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"summarization": f"Request Error: {e}"}
    except Exception as e:
        return {"summarization": f"Error occurred: {e}"}


def chat(query, doc_id: str, url: str = 'http://localhost:5000/chat'):

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'user_query': query,
        'doc_id': doc_id,
    }

    try:
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"answer": f"Error: HTTP {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"answer": f"Request Error: {e}"}
    except Exception as e:
        return {"answer": f"Error occurred: {e}"}

# Contextual Summarization with Retrieval Augmented Generative (RAG) Engine
### KaggleX Final Project

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
   1. [Contextual Summarization](#contextual-summarization)
   2. [Chat with Your Data](#chat-with-your-data)
3. [Getting Started](#getting-started)
   1. [Prerequisites](#prerequisites)
   2. [Installation (Python)](#Installation-via-Python)
   3. [Installation (Docker compose)](#Installation-via-Docker-Compose)
4. [Usage](#usage)
   1. [Python](#Usage-with-Python)
   2. [Docker compose](#Usage-with-Docker-Compose)
5. [Data Privacy](#data-privacy)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgments](#acknowledgments)

## 1. Introduction
Retrieval Augmented Generative (RAG) Engine project! This project combines natural language processing and machine learning to assist users with two key features: Contextual Summarization and Chat with Your Data. This README will provide you with all the information you need to get started and make the most of this project.

## 2. Features

### 2.1 Contextual Summarization
The Contextual Summarization feature allows you to generate concise summaries from various input sources such as web page URLs, text, or documents. It leverages your provided context words to tailor the summarization to your specific needs. Whether you want to quickly understand the essence of an article, extract key points from a document, or summarize any text.

### 2.2 Chat with Your Data
With the Chat with Your Data feature, you can upload your own documents and engage in a conversation with them. Upon uploading your document, you will be assigned a unique ID, which will be active for 48 hours. During this period, you can interact with your data as if you were having a chat, retrieving information, asking questions, or seeking insights. Rest assured that your data will be securely deleted after 48 hours to protect your privacy.

## 3. Getting Started

### 3.1 Prerequisites
Before you get started, ensure you have the following prerequisites:

- Python 3.10.12 installed
- An active internet connection
- Basic knowledge of using the command line

### 3.2 Installation via Python
1. Clone the RAGE project from the GitHub repository:
   ```
   git clone https://github.com/Leumastai/kaggelx-submission.git
   ```

2. Navigate to the project directory:
   ```
   cd kaggelx-submission
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. You're all set!

### 3.3 Installation via Docker Compose
1. Clone the RAGE project from the GitHub repository:
   ```
   git clone https://github.com/Leumastai/kaggelx-submission.git
   ```

2. Install Docker Compose
   ```
   sudo apt-get install software-properties-common && sudo apt-add-repository universe && sudo apt-get update

   sudo apt-get install docker.io
   sudo apt install docker-compose
   pip install docker-compose
   ```

3. Add docker to sudores
   ```
   sudo usermod -aG docker ${USER}
   su - ${USER}
   ```

4. You're all set!

## 4. Usage
### 4.1 Usage with Python
1. Run:
   (In terminal 1)
   ```
   python3 backend/main.py
   ```

   (In terminal 2)
   ```
   python frontend/main.py
   ```

2. Connect to port
   ```
   localhost:8501
   ```


### 4.2 Usage with Docker Compose

To use the Project feature, follow these steps:

1. Run:
   ```
   docker-compose up --build
   ```

2. Connect to port
   ```
   localhost:8501
   ```



## 5. Data Privacy

We take data privacy seriously. Your uploaded documents and chat data will be securely deleted after 48 hours. We do not store any user data beyond this time frame. For more information on data privacy, please refer to our [Privacy Policy](privacy-policy.md).

## 6. Contributing

We welcome contributions from the community. If you'd like to contribute, please check our [Contribution Guidelines](CONTRIBUTING.md).

## 7. License

This project is licensed under the [MIT License](LICENSE).

## 8. Acknowledgments

Thanks to KaggleX for creating such a medium and opportunity that enables individuals to communicate, network, and learn. This platform has been instrumental in the development of this project, and I'm are grateful for the resources and community it provides.

Deep appreciation to Ray and Rainy for their invaluable guidance and support throughout the development project. Thanks once again.


import streamlit as st
import pyperclip
import random
import time

from send_request import contextual_summarization, chat, upload_docs

# Streamlit UI components
st.set_page_config(layout="wide")
st.title("Kaggle X Final Project Submission")

# Contextual Summarization
with st.expander("## **Contextual Summarization**"):
    #st.write("Type of Input:")
    input_type = st.radio("Select Input type:", ["Document", "Text", "Webpage"])

    context_word = st.text_input("Enter context words. Minimum of three words. **E.g FTC\n, California\n, right to repear\n**")

    if input_type == "Document":
        st.write("Upload your document:")
        st.markdown("***PS: This is best use for documents less than 2 pages.***")
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            # Process the uploaded document here
            st.write("Document uploaded:", uploaded_file.name)

            if st.button("Summarize"):
                bot_response = contextual_summarization(
                    selection="file", file_path=uploaded_file, context=context_word)

                summary = bot_response['summarization']
                st.markdown("#### Contextual Summary: \n")
                st.markdown(summary)

                 # Add a "Copy to Clipboard" button
                if st.button("Copy to Clipboard"):
                    pyperclip.copy(bot_response)

    elif input_type == "Text":
        user_input = st.text_area("Enter text here:")

        if st.button("Summarize"):
            if user_input:
                bot_response = contextual_summarization(
                    selection="text", context=context_word, text=user_input)

                summary = bot_response['summarization']
                st.markdown("#### Contextual Summary: \n")
                st.markdown(summary)

                if st.button("Copy to Clipboard"):
                    pyperclip.copy(bot_response)

    elif input_type == "Webpage":
        webpage_url = st.text_input("Enter the URL of the webpage:")
        
        if st.button("Summarize"):
            if webpage_url:
                # Process the URL and retrieve content
                bot_response = contextual_summarization(
                    selection="url", context=context_word, webpage_url=webpage_url)

                summary = bot_response['summarization']
                st.markdown("#### Contextual Summary: \n")
                st.markdown(summary)

                if st.button("Copy to Clipboard"):
                    pyperclip.copy(bot_response)

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating response from API
def generate_llama2_response(prompt_input, doc_id):
    bot_response = chat(query=prompt_input, doc_id=doc_id)
    # bot_response = {"answer": "tpiern"}
    return bot_response


if 'doc_uploaded' not in st.session_state.keys():
    st.session_state.doc_uploaded = False

# if 'doc_id' not in st.session_state.keys():
#     st.session_state.doc_id = False

with st.expander("### **Chat with your Data**", expanded=True):

    has_doc_id = st.radio("Do you have a document id from previous session?", ["", "No", "Yes"], index=0)
    if has_doc_id == "Yes":
        doc_id = st.text_input("Enter your document id here:")
        st.session_state.doc_id = f"{doc_id}" # save doc_id to session
        if st.session_state.doc_id:
            st.session_state.doc_uploaded = True
    
    elif has_doc_id == "No":
        st.markdown("***Upload your document to start chatting***")
        uploaded_file = st.file_uploader("Upload your document to start the conversation...", label_visibility="collapsed")

        if not st.session_state.doc_uploaded and uploaded_file != None:
            #if uploaded_file != None:
                with st.spinner("Upserting document... Sip a cuppa tea 🤗"):
                    user_doc_id = upload_docs(uploaded_file)
                    doc_id = user_doc_id['user_doc_id']
                    # time.sleep(5)
                    # doc_id ="oprempi354"
                    st.session_state.doc_id = f"{doc_id}" # save doc_id to session
        
                if st.session_state.doc_id:
                    st.session_state.doc_uploaded = True
        
        if 'doc_id' in st.session_state.keys():
            st.markdown(f"Your document id is **{st.session_state.doc_id}**. Cached data will be deleted after 48hrs.")
            st.write("You can now start a conversation ...")

print (st.session_state.doc_uploaded)
print ("doing")
if st.session_state.doc_uploaded: #doc_id.strip(): # check if variable is an empty string
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input("User"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                doc_id = st.session_state.doc_id # load doc_id from session.
                response = generate_llama2_response(prompt, doc_id)
                answer = response['answer']
                placeholder = st.empty()
                placeholder.markdown(answer)
        message = {"role": "assistant", "content": answer}
        st.session_state.messages.append(message)

    st.button('Clear Chat History', on_click=clear_chat_history)

# Function to save messages to a text file
def save_messages_to_file():
    if "messages" in st.session_state.keys():
    #if st.session_state.messages:
        with open("chat_history.txt", "w") as file:
            for message in st.session_state.messages:
                file.write(f"{message['role']}: {message['content']}\n")

def download_chat():
    save_messages_to_file()
    with open("chat_history.txt", "r") as file:
        chat_history_text = file.read()

    return chat_history_text

if st.download_button(
    label="Download Chat History",
    data= download_chat(),
    key="download_button",
    file_name="chat_history.txt",
):
    pass

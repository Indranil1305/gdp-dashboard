import streamlit as st
import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI

load_dotenv()

# Front end
st.title("AskNotes.ai")

# File Uploader
pdfs = st.file_uploader(label="Upload PDF", accept_multiple_files=True, type='.pdf')

# Create new directory
newpath = r'D:\VSCodePrograms\AskNotes\Asknotes\DataFiles'  # Adjust path as needed
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Copy PDFs to new directory
for pdf in pdfs:
    try:
        file_path = os.path.join(newpath, pdf.name)
        with open(file_path, 'wb') as f:
            f.write(pdf.getbuffer())
    except Exception as e:
        st.write(f'Error copying {pdf.name}: {e}')

# Prompt input
prompt = st.text_input("Enter your prompt")
if prompt:
    loader = PyPDFLoader(newpath)
    index = VectorstoreIndexCreator().from_loaders([loader])

    # Initialize ChatOpenAI
    llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.6)

    # Query and display response
    response = index.query(prompt)
    st.write(response)
    print(response)

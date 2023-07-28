from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 📑")

    pdf = st.file_uploader("Upload your PDF", type="pdf")
    if pdf is not None:
        pdf_doc = PdfReader(pdf)
        text = "" 
        for page in pdf_doc.pages:
            text += page.extract_text()

        text_spliiter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=15, length_function=len)
        chunks = text_spliiter.split_text(text)

        embeddings = OpenAIEmbeddings()
        documents = FAISS.from_texts(chunks, embeddings)

        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            # Perform similarity search to get relevant documents for the user's question
            docs = documents.similarity_search(user_question)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")

            # Perform question answering using the defined chain
            response = chain.run(input_documents=docs, question=user_question)
            st.write(response)

if __name__ == "__main__":
    main()

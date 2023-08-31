from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from prompt import get_completion


def contradict(answer):
    #user_q = st.text_input(label = "", key="new_input", placeholder="Ask a question about your PDF:")
    

    prompt = answer + "\n" + "Given above are a list of requirements from a client for a company that builds EV charging software. Point out which of these statements might be contradictory to each other, along with scenarios of failure"
    final_ans = get_completion(prompt)
    res = final_ans
    return res
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
        ans = ""
        if user_question:
            # Perform similarity search to get relevant documents for the user's question
            docs = documents.similarity_search(user_question)

            

            
            llm = OpenAI()
            #chain = load_qa_chain(llm, chain_type="stuff")
            qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=documents.as_retriever(), return_source_documents=True)
            result = qa({"query":user_question})
            ans+=result["result"]

            st.write(result["result"])
           
    

    resp = st.button("Generate Contradictions")

    if resp:
        
        if ans == "":
            st.write("No context provided. Please ask an appropriate question")
        else:
            resp = contradict(ans)
            st.write(resp)
            
            
if __name__ == "__main__":
    main()

import os
import time
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from context_builder_v1 import build_context
from metrics import Metrics

load_dotenv()
 
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

embeddings = OpenAIEmbeddings()
vector_db = Chroma(persist_directory="db", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 20})
print("Vector store loaded.")
print("Retriever:", retriever)

def ask_question(query):
    metrics = Metrics()

    context, retrieval_time = build_context(retriever, query)
    

    print("----- CONTEXT RETRIEVED -----")
    print(context[:1000])  # print first 1000 chars
    print("-----------------------------")

    prompt = f"""
You are an assistant. Answer the question using only the context below.

Context:
{context}

Question:
{query}
"""
    start_llm = time.time()
    response = llm.invoke(prompt)
    llm_time = time.time() - start_llm

    metrics.stop()

    print("\nAnswer:\n", response.content)
    print("\n--- Metrics ---")
    print("Retrieval time:", round(retrieval_time,2), "sec")
    print("LLM time:", round(llm_time,2), "sec")
    print("Total latency:", metrics.latency, "sec")

if __name__ == "__main__":
    while True:
        q = input("\nAsk question (or 'exit'): ")
        if q.lower() == "exit":
            break
        ask_question(q)
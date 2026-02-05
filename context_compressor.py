from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

compressor_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def compress_context(query: str, docs, max_words=150):
    """
    Compress each retrieved document to only what is relevant to the query.
    """
    compressed_chunks = []

    for doc in docs:
        prompt = f"""
You are a context compression engine.

Question:
{query}

Document:
{doc.page_content}

Extract ONLY the information relevant to answering the question.
Do not add new information.
Limit output to {max_words} words.
If nothing is relevant, return "NOT_RELEVANT".
"""

        summary = compressor_llm.invoke(prompt).content.strip()

        if summary != "NOT_RELEVANT":
            compressed_chunks.append(summary)

    return compressed_chunks
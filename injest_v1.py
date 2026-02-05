from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

DB_DIR = "db"
DATA_FILE = "/Users/manishmaurya/Desktop/OpenAIApplications/contextualisingModelapp/rag/data.txt"

# Load full document
loader = TextLoader(DATA_FILE, encoding="utf-8")
text = loader.load()[0].page_content

# Semantic split by sections
sections = re.split(r"=+|Section \d+:", text)

docs = []
for section in sections:
    cleaned = section.strip()
    if len(cleaned) > 100:
        docs.append(Document(page_content=cleaned))

print("Total semantic chunks:", len(docs))

# Delete old DB
if os.path.exists(DB_DIR):
    import shutil
    shutil.rmtree(DB_DIR)

embeddings = OpenAIEmbeddings()

vector_db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=DB_DIR
)

vector_db.persist()
print("Vector DB created with semantic chunks.")
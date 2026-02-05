from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
file_path = "/Users/manishmaurya/Desktop/OpenAIApplications/contextualisingModelapp/rag/docs.txt"
print("File exists:", os.path.exists(file_path))
print("Absolute path:", os.path.abspath(file_path))
loader = TextLoader("/Users/manishmaurya/Desktop/OpenAIApplications/contextualisingModelapp/rag/docs.txt")
documents = loader.load()

print("Loaded documents:", len(documents))

splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
chunks = splitter.split_documents(documents)

print("Total chunks:", len(chunks))

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="db"
)

vector_db.persist()
print("Vector DB created and persisted.")
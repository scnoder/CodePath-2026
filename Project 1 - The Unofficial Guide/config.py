import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHROMA_COLLECTION = "lincolnbot"
CHROMA_PATH = "./chroma_db"

N_RESULTS = 3

DOCS_PATH = "./documents"

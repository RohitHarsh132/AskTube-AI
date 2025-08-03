from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

def split_text(text: str, chunk_size=1000, chunk_overlap=200):
    """
    Split text into chunks with better parameters for RAG
    - Larger chunks (1000 chars) for better context
    - More overlap (200 chars) to avoid missing information at boundaries
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    )
    return splitter.create_documents([text])

def setup_vector_store(video_id: str, texts):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    collection_name = f"video_{video_id}"
    persist_dir = os.getenv("CHROMA_DB_PATH", "./chroma_langchain_db")

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )

    # Avoid duplicate insert
    if len(vector_store.get()["ids"]) == 0:
        vector_store.add_documents(texts)

    # Use hybrid search: combination of similarity and keyword search
    retriever = vector_store.as_retriever(
        search_type="mmr",  # Maximum Marginal Relevance - better diversity
        search_kwargs={
            "k": 15,  # Get more candidates
            "fetch_k": 30,  # Fetch more for better selection
            "lambda_mult": 0.7  # Balance between relevance and diversity
        }
    )
    return retriever
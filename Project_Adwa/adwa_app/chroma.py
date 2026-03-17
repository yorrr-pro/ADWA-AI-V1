import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Use Google API (requires GOOGLE_API_KEY in environment variables)
_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

_persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")

_vector_store = Chroma(
    persist_directory=_persist_dir,
    embedding_function=_embeddings
)

_retriever = _vector_store.as_retriever(search_kwargs={"k": 6})

class Retriever:
    def __init__(self, query):
        self.retrieved = _retriever.invoke(query)
        self.context = "\n\n".join([r.page_content for r in self.retrieved])
    
    def chroma_result(self):
        meta = [r.metadata for r in self.retrieved]
        return self.context, meta

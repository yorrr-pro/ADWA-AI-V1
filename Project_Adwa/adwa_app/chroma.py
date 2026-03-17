import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class Retriever:
    _vector_store = None
    _retriever = None

    def __init__(self, query):
        self.query = query
        # Lazy-load vector store and embeddings
        if not Retriever._vector_store:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
            Retriever._vector_store = Chroma(
                persist_directory=persist_dir,
                embedding_function=embeddings
            )
            # Reduce 'k' to 3 to save memory
            Retriever._retriever = Retriever._vector_store.as_retriever(search_kwargs={"k": 3})
        
        # Perform retrieval
        self.retrieved = Retriever._retriever.invoke(self.query)
        self.context = "\n\n".join([r.page_content for r in self.retrieved])

    def chroma_result(self):
        meta = [r.metadata for r in self.retrieved]
        return self.context, meta
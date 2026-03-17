# import os
# from langchain_chroma import Chroma
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Global lazy-loaded vector store
# _vector_store = None
# _retriever = None

# def get_retriever():
#     global _vector_store, _retriever
#     if not _vector_store:
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
#         _vector_store = Chroma(
#             persist_directory=persist_dir,
#             embedding_function=embeddings
#         )
#         _retriever = _vector_store.as_retriever(search_kwargs={"k": 2})  # lower k to save memory
#     return _retriever

# class Retriever:
#     def __init__(self, query):
#         self.query = query
#         retriever = get_retriever()
#         self.retrieved = retriever.invoke(self.query)
#         self.context = "\n\n".join([r.page_content for r in self.retrieved])

#     def chroma_result(self):
#         meta = [r.metadata for r in self.retrieved]
#         return self.context, meta
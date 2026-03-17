import os
import dotenv
from .chroma import Retriever
from .serper import Serper
from google import genai

dotenv.load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api)

_chat_memory = {}

class Response:
    def __init__(self, query, context_s, context_r, session_id="default"):
        history = _chat_memory.get(session_id, [])
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        self.prompt = f"""
User question: {query}

Book Context: {context_r}
Web Results: {context_s}
Conversation History: {history_text}
"""
        self.response_text = "No answer available."

        try:
            # Gemini call
            res = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=self.prompt
            )
            self.response_text = res.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            self.response_text = "AI service is currently unavailable."

    def respond(self):
        return self.response_text

class My_AI:
    _chroma_cache = {}

    def __init__(self, question):
        # Chroma
        try:
            if question in My_AI._chroma_cache:
                context, meta = My_AI._chroma_cache[question]
            else:
                chroma = Retriever(question)
                context, meta = chroma.chroma_result()
                My_AI._chroma_cache[question] = (context, meta)
        except Exception as e:
            print(f"Chroma error: {e}")
            context = ""
            meta = []

        # Serper
        try:
            serper = Serper(question)
            search_result, serper_sources = serper.serper_result()
        except Exception as e:
            print(f"Serper error: {e}")
            search_result = []
            serper_sources = []

        # Gemini / Response
        gemini = Response(query=question, context_s=search_result, context_r=context)

        self.sources = {"source": serper_sources}
        self.final_answer = {"answer": gemini.respond()}

    def answer(self):
        return self.final_answer, self.sources
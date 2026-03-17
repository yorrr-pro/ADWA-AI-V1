from .chroma import Retriever
from .serper import Serper
from google import genai
import os
import dotenv

dotenv.load_dotenv()

gemini_api = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api)

_chat_memory = {}


class Response:
    def __init__(self, query, context_s, context_r, session_id="default"):
        history = _chat_memory.get(session_id, [])
        history_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in history]
        )
        self.prompt = f"""
# 🎖️ Ultimate AdwaBot — Flexible Prompt (ready for .py)

User question:
{query}

Book Context (primary):
{context_r}

Web Results (support only):
{context_s}

Conversation history:
{history_text}
"""
        self.response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=self.prompt,
        )

    def respond(self):
        return self.response.text


class My_AI:
    _chroma_cache = {}  # Cache to reuse context for repeated queries

    def __init__(self, question):
        # Use cached Chroma context if available
        if question in My_AI._chroma_cache:
            context, meta = My_AI._chroma_cache[question]
        else:
            chroma = Retriever(question)
            context, meta = chroma.chroma_result()
            My_AI._chroma_cache[question] = (context, meta)

        # Get web search results via Serper
        serper = Serper(question)
        search_result, serper_sources = serper.serper_result()

        # Generate final response via Gemini AI
        gemini = Response(query=question, context_s=search_result, context_r=context)

        self.sources = {"source": serper_sources}
        self.final_answer = {"answer": gemini.respond()}

    def answer(self):
        return self.final_answer, self.sources


# -----------------------------
# Optional testing/debug block
# -----------------------------
# while True:
#     question = input("Ask about Adwa: ")
#     ai = My_AI(question)
#     print("Answer:\n", ai.answer()[0]["answer"])
#     print("Sources:\n", ai.answer()[1]["source"])
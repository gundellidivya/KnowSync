from backend.vector_store import query_chunks
from backend.llm import ask_llm

def rag_answer(question: str) -> str:
    chunks = query_chunks(question, top_k=3)

    context = "\n\n".join(chunks)

    prompt = f"""
You are an AI assistant.
Answer the question ONLY using the context below.
If the answer is not in the context, say "Information not found in the provided documents."

Context:
{context}

Question:
{question}
"""

    return ask_llm(prompt)

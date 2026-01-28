from backend.content_loader import load_file_content
from backend.chunker import chunk_text
from backend.vector_store import (
    create_temp_collection,
    store_chunks,
    query_chunks
)
from backend.llm import ask_llm

def answer_from_file(file_path: str, question: str) -> str:
    text = load_file_content(file_path)

    if not text.strip():
        return "Unable to read content from the file."

    chunks = chunk_text(text)

    # NEW: isolated vector collection
    collection = create_temp_collection()
    store_chunks(collection, chunks)

    relevant_chunks = query_chunks(collection, question)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an assistant.
Answer STRICTLY using the context below.
Do NOT add outside knowledge.
If the answer is not in the context, say:
"Information not found in this file."

Context:
{context}

Question:
{question}
"""

    return ask_llm(prompt)

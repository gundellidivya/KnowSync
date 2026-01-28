import requests
import chromadb

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "tinyllama"

def get_embedding(text: str):
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]


def create_temp_collection():
    client = chromadb.Client()
    return client.create_collection(name="temp_docs")


def store_chunks(collection, chunks):
    embeddings = [get_embedding(c) for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )


def query_chunks(collection, query, top_k=3):
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]

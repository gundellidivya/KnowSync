def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    """
    Splits text into overlapping chunks.
    chunk_size: number of characters per chunk
    overlap: number of characters shared between chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

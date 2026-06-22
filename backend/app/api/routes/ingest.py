from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import tempfile
import os

router = APIRouter()


@router.post("/")
async def ingest_document(files: List[UploadFile] = File(...)):
    """Upload and embed documents into the RAG knowledge base."""
    from app.core.config import settings
    import chromadb
    from openai import OpenAI

    results = []
    client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
    collection = client.get_or_create_collection(settings.CHROMA_COLLECTION)
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    for file in files:
        try:
            content = await file.read()
            text = content.decode("utf-8")

            # Chunk the document
            chunks = _chunk_text(text, chunk_size=500, overlap=50)

            embeddings = []
            for chunk in chunks:
                resp = openai_client.embeddings.create(model=settings.EMBEDDING_MODEL, input=chunk)
                embeddings.append(resp.data[0].embedding)

            ids = [f"{file.filename}_{i}" for i in range(len(chunks))]
            metadatas = [{"source": file.filename, "chunk": i} for i in range(len(chunks))]

            collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
            results.append({"file": file.filename, "chunks": len(chunks), "status": "ingested"})

        except Exception as e:
            results.append({"file": file.filename, "status": "error", "detail": str(e)})

    return {"results": results}


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Simple word-based chunking with overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

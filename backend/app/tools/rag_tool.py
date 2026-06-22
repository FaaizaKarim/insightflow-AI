"""
RAG Search Tool — semantic search over company policy documents using ChromaDB.
"""
from langchain_core.tools import tool
from app.core.config import settings


def get_chroma_client():
    import chromadb
    client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
    return client


def get_embedding(text: str) -> list[float]:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


@tool
def rag_search_tool(query: str) -> str:
    """
    Search company policy documents, FAQs, SLAs, and internal knowledge base using semantic search.
    Use this for questions about company policies, refund rules, procedures, compliance, or contracts.
    
    Args:
        query: The question or topic to search for in company documents.
    
    Returns:
        Relevant document excerpts with source citations.
    """
    try:
        client = get_chroma_client()
        collection = client.get_or_create_collection(settings.CHROMA_COLLECTION)

        # Get query embedding
        query_embedding = get_embedding(query)

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"][0]:
            return "No relevant documents found. The knowledge base may be empty — run the document ingestion pipeline."

        lines = [f"**Document Search Results for:** '{query}'\n"]
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )):
            relevance = round((1 - dist) * 100, 1)
            source = meta.get("source", "Unknown document")
            section = meta.get("section", "")
            lines.append(
                f"**[{i+1}] Source: {source}** {f'— {section}' if section else ''} "
                f"(Relevance: {relevance}%)\n\n{doc}\n"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"RAG search error: {str(e)}"

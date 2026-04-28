"""
QuickShop AI - RAG Engine (Unstructured Data)
Handles PDF ingestion, embedding via Vertex AI, and semantic search via ChromaDB.
"""

import os
import tempfile
from typing import List, Dict
from google.cloud import storage
from pypdf import PdfReader
import chromadb
from chromadb.config import Settings as ChromaSettings
import vertexai
from vertexai.language_models import TextEmbeddingModel

from config import get_settings

settings = get_settings()

_embedding_model: TextEmbeddingModel | None = None
_chroma_client = None
_collection = None


def _get_embedding_model() -> TextEmbeddingModel:
    """Lazy-load Vertex AI embedding model (text-embedding-004)."""
    global _embedding_model
    if _embedding_model is None:
        vertexai.init(project=settings.gcp_project_id, location=settings.gcp_region)
        _embedding_model = TextEmbeddingModel.from_pretrained(settings.embedding_model)
    return _embedding_model


def _embed_texts(texts: List[str]) -> List[List[float]]:
    """Get embeddings from Vertex AI in batches."""
    model = _get_embedding_model()
    embeddings = []
    # Vertex AI accepts up to 5 texts per request for this model
    batch_size = 5
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        result = model.get_embeddings(batch)
        embeddings.extend([emb.values for emb in result])
    return embeddings


def _get_chroma_collection():
    """Lazy-init ChromaDB collection (in-memory)."""
    global _chroma_client, _collection
    if _chroma_client is None:
        _chroma_client = chromadb.Client(ChromaSettings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        _collection = _chroma_client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks (sliding window)."""
    if not text:
        return []
    words = text.split()
    chunks = []
    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def _download_pdfs_from_gcs() -> List[Dict[str, str]]:
    """Download all PDFs from the GCS documents/ folder."""
    client = storage.Client(project=settings.gcp_project_id)
    bucket = client.bucket(settings.gcs_bucket_name)
    blobs = bucket.list_blobs(prefix=settings.documents_prefix)

    docs = []
    for blob in blobs:
        if not blob.name.lower().endswith('.pdf'):
            continue
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            blob.download_to_filename(tmp.name)
            try:
                reader = PdfReader(tmp.name)
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text() + "\n"
                docs.append({
                    "name": os.path.basename(blob.name),
                    "text": full_text.strip()
                })
            finally:
                os.unlink(tmp.name)
    return docs


def ingest_documents() -> int:
    """Pull PDFs from GCS, chunk, embed via Vertex AI, store in ChromaDB."""
    # Reset collection
    global _chroma_client, _collection
    if _chroma_client is None:
        _get_chroma_collection()
    try:
        _chroma_client.delete_collection(settings.chroma_collection_name)
    except Exception:
        pass
    _collection = _chroma_client.get_or_create_collection(
        name=settings.chroma_collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    collection = _collection

    docs = _download_pdfs_from_gcs()
    total_chunks = 0

    for doc in docs:
        chunks = _chunk_text(doc["text"], settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            continue
        embeddings = _embed_texts(chunks)
        ids = [f"{doc['name']}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc["name"], "chunk_index": i} for i in range(len(chunks))]
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )
        total_chunks += len(chunks)
        print(f"✓ Ingested {doc['name']}: {len(chunks)} chunks")

    print(f"\n✓ Total chunks in ChromaDB: {total_chunks}")
    return total_chunks


def search(query: str, top_k: int | None = None) -> List[Dict]:
    """Search the vector store for semantically similar chunks."""
    collection = _get_chroma_collection()

    if collection.count() == 0:
        return []

    k = top_k or settings.top_k_chunks
    query_emb = _embed_texts([query])[0]
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=k
    )

    out = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, dist in zip(docs, metas, distances):
        out.append({
            "text": doc,
            "source": meta.get("source", "unknown"),
            "score": round(1 - dist, 3)
        })
    return out


def get_stats() -> Dict:
    """Return collection stats."""
    collection = _get_chroma_collection()
    return {
        "total_chunks": collection.count(),
        "collection_name": settings.chroma_collection_name
    }

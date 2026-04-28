"""
QuickShop AI - FastAPI Application
Main API server. Deployed on Cloud Run.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

from config import get_settings
import database
import rag_engine
import router as query_router

# ============================================
# Logging
# ============================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

settings = get_settings()


# ============================================
# Lifespan: ingest docs at startup
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 QuickShop AI starting up...")
    try:
        # Test DB connectivity
        if database.health_check():
            logger.info("✓ Cloud SQL connected")
        else:
            logger.warning("✗ Cloud SQL connection failed (will retry per-request)")

        # Ingest PDFs into ChromaDB
        logger.info("Ingesting documents from GCS...")
        chunk_count = rag_engine.ingest_documents()
        logger.info(f"✓ Ingested {chunk_count} chunks into ChromaDB")
    except Exception as e:
        logger.error(f"Startup error: {e}")
    yield
    logger.info("Shutting down.")


# ============================================
# App
# ============================================
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Schemas
# ============================================
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)


class ChatResponse(BaseModel):
    answer: str
    route: str
    sources: List[str] = []
    sql: Optional[str] = None
    results_count: int = 0


# ============================================
# Endpoints
# ============================================
@app.get("/")
def root():
    return {
        "service": settings.api_title,
        "version": settings.api_version,
        "status": "running",
        "endpoints": ["/chat", "/health", "/stats", "/ingest"]
    }


@app.get("/health")
def health():
    db_ok = database.health_check()
    rag_stats = rag_engine.get_stats()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "ok" if db_ok else "error",
        "rag_chunks": rag_stats["total_chunks"]
    }


@app.get("/stats")
def stats():
    rag_stats = rag_engine.get_stats()
    return {
        "rag": rag_stats,
        "model": settings.gemini_model,
        "region": settings.gcp_region
    }


@app.post("/ingest")
def ingest():
    """Re-ingest PDFs from GCS. Useful after uploading new documents."""
    try:
        count = rag_engine.ingest_documents()
        return {"status": "success", "chunks_ingested": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Main chat endpoint - routes to RAG, SQL, or both."""
    try:
        result = query_router.handle_query(req.message)
        return ChatResponse(**result)
    except Exception as e:
        logger.exception("Chat error")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Local run
# ============================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

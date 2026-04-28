"""
QuickShop AI - Centralized Configuration
All environment variables and settings live here.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # ============================================
    # GCP Project Settings
    # ============================================
    gcp_project_id: str = "project-c5185bee-a238-4d53-b9b"
    gcp_region: str = "asia-south1"
    
    # ============================================
    # Cloud SQL Settings
    # ============================================
    db_instance_connection_name: str = "project-c5185bee-a238-4d53-b9b:asia-south1:quickshop-db"
    db_user: str = "postgres"
    db_password: str = ""  # Loaded from .env
    db_name: str = "quickshop"
    
    # ============================================
    # GCS Settings
    # ============================================
    gcs_bucket_name: str = "quickshop-docs-1777287829"
    documents_prefix: str = "documents/"
    
    # ============================================
    # Vertex AI / Gemini Settings
    # ============================================
    gemini_model: str = "gemini-2.5-flash"  # Fast & free quota
    embedding_model: str = "text-embedding-004"
    
    # ============================================
    # ChromaDB Settings (in-memory vector store)
    # ============================================
    chroma_collection_name: str = "quickshop_docs"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_chunks: int = 3
    
    # ============================================
    # API Settings
    # ============================================
    api_title: str = "QuickShop AI Backend"
    api_version: str = "1.0.0"
    cors_origins: list = ["*"]  # Tighten in production
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings - load once, reuse everywhere."""
    return Settings()

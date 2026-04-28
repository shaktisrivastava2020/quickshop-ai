"""
QuickShop AI - NL2SQL Engine (Structured Data)
Converts natural language to SQL using Gemini, executes on Cloud SQL.
"""

import re
from typing import Dict, List
import vertexai
from vertexai.generative_models import GenerativeModel

from config import get_settings
from database import execute_query, get_table_schema

settings = get_settings()

# Singleton model instance
_model: GenerativeModel | None = None


def _get_model() -> GenerativeModel:
    """Lazy-init the Gemini model."""
    global _model
    if _model is None:
        vertexai.init(project=settings.gcp_project_id, location=settings.gcp_region)
        _model = GenerativeModel(settings.gemini_model)
    return _model


# ============================================
# Safety: block destructive SQL
# ============================================
DANGEROUS_KEYWORDS = [
    'DROP', 'DELETE', 'TRUNCATE', 'INSERT', 'UPDATE',
    'ALTER', 'CREATE', 'GRANT', 'REVOKE', 'EXEC'
]


def _is_safe_sql(sql: str) -> bool:
    """Reject anything that's not a pure SELECT."""
    sql_upper = sql.upper().strip()
    if not sql_upper.startswith('SELECT') and not sql_upper.startswith('WITH'):
        return False
    for keyword in DANGEROUS_KEYWORDS:
        if re.search(rf'\b{keyword}\b', sql_upper):
            return False
    return True


def _extract_sql(response_text: str) -> str:
    """Extract SQL from Gemini's response (handles ```sql code blocks)."""
    # Try fenced code block first
    m = re.search(r'```(?:sql)?\s*(.*?)```', response_text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip().rstrip(';')
    # Fallback: take everything from SELECT onward
    m = re.search(r'(SELECT|WITH)\s+.+', response_text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(0).strip().rstrip(';')
    return response_text.strip().rstrip(';')


def generate_sql(question: str) -> str:
    """Use Gemini to convert a natural-language question into PostgreSQL SQL."""
    schema = get_table_schema()
    prompt = f"""You are an expert PostgreSQL query writer for QuickShop AI, an Indian e-commerce platform.

{schema}

RULES:
1. Generate ONLY a SELECT query (read-only).
2. Use proper PostgreSQL syntax.
3. Use JOINs when querying across tables.
4. Always LIMIT results to 50 rows max unless user asks for a count/aggregate.
5. For "recent" or "latest" queries, ORDER BY date DESC.
6. Use ILIKE for case-insensitive text matching.
7. Return ONLY the SQL query, wrapped in ```sql ... ``` code block.
8. Do NOT include any explanation.

USER QUESTION: {question}

SQL:"""

    model = _get_model()
    response = model.generate_content(prompt)
    sql = _extract_sql(response.text)
    return sql


def query(question: str) -> Dict:
    """
    Full NL2SQL pipeline: question -> SQL -> execute -> results.
    Returns {sql, results, error?}.
    """
    try:
        sql = generate_sql(question)
    except Exception as e:
        return {"sql": None, "results": [], "error": f"SQL generation failed: {e}"}

    if not _is_safe_sql(sql):
        return {
            "sql": sql,
            "results": [],
            "error": "Generated SQL was blocked for safety (only SELECT queries allowed)."
        }

    try:
        results = execute_query(sql)
        # Convert any Decimal/Date objects to strings for JSON serialization
        cleaned = []
        for row in results:
            cleaned.append({k: str(v) if v is not None else None for k, v in row.items()})
        return {"sql": sql, "results": cleaned, "error": None}
    except Exception as e:
        return {"sql": sql, "results": [], "error": f"SQL execution failed: {e}"}


def format_results_as_text(results: List[Dict], max_rows: int = 10) -> str:
    """Format SQL results as a readable string for the LLM to summarize."""
    if not results:
        return "No matching records found."
    
    lines = [f"Query returned {len(results)} row(s) of data:"]
    if len(results) > max_rows:
        lines.append(f"Showing first {max_rows}:")
        results = results[:max_rows]
    
    for i, row in enumerate(results, 1):
        row_str = ", ".join([f"{k}: {v}" for k, v in row.items()])
        lines.append(f"{i}. {row_str}")
    return "\n".join(lines)

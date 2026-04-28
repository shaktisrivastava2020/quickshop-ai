"""
QuickShop AI - Smart Query Router
Classifies user questions and routes to RAG (docs) or SQL (data) or BOTH.
Then synthesizes a final answer using Gemini.
"""

import json
import re
from typing import Dict
import vertexai
from vertexai.generative_models import GenerativeModel

from config import get_settings
import rag_engine
import sql_engine

settings = get_settings()

_model: GenerativeModel | None = None


def _get_model() -> GenerativeModel:
    global _model
    if _model is None:
        vertexai.init(project=settings.gcp_project_id, location=settings.gcp_region)
        _model = GenerativeModel(settings.gemini_model)
    return _model


def classify_question(question: str) -> str:
    """
    Classify the question into: 'rag', 'sql', or 'both'.
    - rag  -> policy/FAQ questions (return policy, shipping, warranty)
    - sql  -> data questions (orders, products, customers, inventory)
    - both -> mixed questions
    """
    prompt = f"""You are a query classifier for QuickShop AI, an e-commerce assistant.

Classify the user's question into ONE of these categories:

1. "rag" — questions about policies, FAQs, shipping rules, return rules, warranty, customer service hours.
   Examples: "What is your return policy?", "How long does shipping take?", "Is my product under warranty?"

2. "sql" — questions about specific data: orders, products, customers, inventory, prices, stock levels, sales numbers.
   Examples: "Show me top 5 orders", "How many customers in Mumbai?", "What's in stock for headphones?"

3. "both" — questions that need BOTH policy info AND data lookup.
   Examples: "What's your refund policy and how many refunds last month?", "Tell me about shipping and how many orders are pending."

USER QUESTION: {question}

Respond with ONLY one word: rag, sql, or both."""

    model = _get_model()
    response = model.generate_content(prompt)
    label = response.text.strip().lower()
    # Extract just the label word
    label = re.sub(r'[^a-z]', '', label)
    if label not in ['rag', 'sql', 'both']:
        # Default to 'both' if unsure
        return 'both'
    return label


def synthesize_answer(question: str, rag_context: str, sql_context: str) -> str:
    """
    Combine RAG + SQL context into a final natural-language answer using Gemini.
    """
    prompt = f"""You are QuickShop AI's helpful customer assistant.
Answer the user's question using ONLY the provided context. Be concise, friendly, and clear. The DATA CONTEXT contains the actual answer - trust it and present it confidently. If you see "count" or "COUNT" in results, that IS the answer to the user's counting question.
If the context doesn't contain the answer, say so honestly.

USER QUESTION: {question}

POLICY/FAQ CONTEXT:
{rag_context if rag_context else '(none)'}

DATA CONTEXT:
{sql_context if sql_context else '(none)'}

INSTRUCTIONS:
- Use Indian Rupee symbol (₹) for currency.
- If you used data, briefly mention how many records were found.
- If you used policy info, cite the source PDF (e.g., "per our return policy").
- Keep the answer under 150 words.
- Do NOT make up information not in the context.

ANSWER:"""

    model = _get_model()
    response = model.generate_content(prompt)
    return response.text.strip()


def handle_query(question: str) -> Dict:
    """
    Main entry point. Routes the question, gathers context, synthesizes answer.
    Returns {answer, route, sources, sql, results_count}.
    """
    route = classify_question(question)

    rag_context = ""
    sql_context = ""
    sources = []
    sql_query = None
    results_count = 0

    # RAG branch
    if route in ('rag', 'both'):
        rag_results = rag_engine.search(question)
        if rag_results:
            rag_context = "\n\n".join([
                f"[Source: {r['source']}]\n{r['text']}" for r in rag_results
            ])
            sources = list(set([r['source'] for r in rag_results]))

    # SQL branch
    if route in ('sql', 'both'):
        sql_result = sql_engine.query(question)
        sql_query = sql_result.get('sql')
        if sql_result.get('error'):
            sql_context = f"(SQL error: {sql_result['error']})"
        else:
            sql_context = sql_engine.format_results_as_text(sql_result['results'])
            results_count = len(sql_result['results'])

    answer = synthesize_answer(question, rag_context, sql_context)

    return {
        "answer": answer,
        "route": route,
        "sources": sources,
        "sql": sql_query,
        "results_count": results_count
    }

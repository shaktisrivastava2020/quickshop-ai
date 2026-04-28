/**
 * QuickShop AI - API Client
 * Handles all backend communication
 */

// API URL - reads from env (Cloud Run) or falls back to localhost (dev)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export interface ChatResponse {
  answer: string;
  route: 'rag' | 'sql' | 'both';
  sources: string[];
  sql: string | null;
  results_count: number;
}

export interface HealthResponse {
  status: string;
  database: string;
  rag_chunks: number;
}

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_URL}/health`);
  return res.json();
}

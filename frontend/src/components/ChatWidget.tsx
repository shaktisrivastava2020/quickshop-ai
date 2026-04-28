import { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../lib/api';
import type { ChatResponse } from '../lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  sql?: string | null;
  route?: string;
  results_count?: number;
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hi! I'm QuickShop AI 👋 Ask me about our products, orders, return policy, shipping, or anything else!",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSqlFor, setShowSqlFor] = useState<number | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, loading]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg: Message = { role: 'user', content: input };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res: ChatResponse = await sendChatMessage(userMsg.content);
      setMessages((m) => [
        ...m,
        {
          role: 'assistant',
          content: res.answer,
          sources: res.sources,
          sql: res.sql,
          route: res.route,
          results_count: res.results_count,
        },
      ]);
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: '⚠️ Sorry, I had trouble connecting. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const sampleQuestions = [
    'What is your return policy?',
    'Show me top 5 products by price',
    'How many orders are pending?',
    'What is your shipping policy and how many delivered orders?',
  ];

  return (
    <>
      {/* Floating Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 w-16 h-16 rounded-full bg-primary hover:bg-primary-dark text-white shadow-medium flex items-center justify-center transition-all hover:scale-110 z-50"
          aria-label="Open chat"
        >
          <svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}

      {/* Chat Panel */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-[400px] h-[600px] max-h-[85vh] bg-white rounded-2xl shadow-medium flex flex-col overflow-hidden animate-slide-up z-50">
          {/* Header */}
          <div className="bg-gradient-to-r from-primary to-primary-dark text-white p-4 flex items-center justify-between">
            <div>
              <div className="font-semibold text-lg">QuickShop AI</div>
              <div className="text-xs opacity-90 flex items-center gap-1">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse-slow"></span>
                AI Assistant • Online
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-white/20 rounded-full p-1.5" aria-label="Close">
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3 chat-scroll">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-2xl px-4 py-2.5 ${
                  m.role === 'user'
                    ? 'bg-primary text-white rounded-br-sm'
                    : 'bg-gray-100 text-gray-800 rounded-bl-sm'
                }`}>
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">{m.content}</div>
                  
                  {/* Source citations */}
                  {m.sources && m.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-200 flex flex-wrap gap-1.5">
                      {m.sources.map((s, idx) => (
                        <span key={idx} className="text-[10px] bg-white text-gray-600 px-2 py-0.5 rounded-full border border-gray-200">
                          📄 {s}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Route badge + SQL toggle */}
                  {m.route && (
                    <div className="mt-2 flex items-center gap-2 flex-wrap">
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                        m.route === 'rag' ? 'bg-blue-100 text-blue-700' :
                        m.route === 'sql' ? 'bg-purple-100 text-purple-700' :
                        'bg-amber-100 text-amber-700'
                      }`}>
                        {m.route === 'rag' ? '📚 Docs' : m.route === 'sql' ? '🗄️ Database' : '🔀 Hybrid'}
                      </span>
                      {m.sql && (
                        <button
                          onClick={() => setShowSqlFor(showSqlFor === i ? null : i)}
                          className="text-[10px] text-gray-600 hover:text-primary underline"
                        >
                          {showSqlFor === i ? 'Hide SQL' : 'View SQL'}
                        </button>
                      )}
                    </div>
                  )}
                  {m.sql && showSqlFor === i && (
                    <pre className="mt-2 p-2 bg-gray-900 text-green-400 text-[10px] rounded overflow-x-auto">{m.sql}</pre>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                </div>
              </div>
            )}

            {/* Sample questions */}
            {messages.length === 1 && (
              <div className="space-y-1.5 pt-2">
                <div className="text-[11px] text-gray-500 font-medium">Try asking:</div>
                {sampleQuestions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(q)}
                    className="block w-full text-left text-xs bg-primary-light hover:bg-blue-100 text-primary px-3 py-2 rounded-lg transition"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-3 bg-gray-50">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && send()}
                placeholder="Ask anything about products, orders, or policies..."
                disabled={loading}
                className="flex-1 px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:border-primary disabled:opacity-60"
              />
              <button
                onClick={send}
                disabled={loading || !input.trim()}
                className="bg-primary hover:bg-primary-dark text-white px-4 rounded-lg transition disabled:opacity-50"
              >
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M2 21l21-9L2 3v7l15 2-15 2z" />
                </svg>
              </button>
            </div>
            <div className="text-[10px] text-gray-400 mt-1.5 text-center">
              Powered by Vertex AI Gemini • Cloud SQL • ChromaDB
            </div>
          </div>
        </div>
      )}
    </>
  );
}

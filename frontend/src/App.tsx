import ChatWidget from './components/ChatWidget';

const featuredProducts = [
  { id: 1, name: 'Boat Smart Watch Storm Pro', price: 2499, originalPrice: 3999, category: 'Electronics', emoji: '⌚', rating: 4.5 },
  { id: 2, name: 'Mamaearth Vitamin C Serum', price: 599, originalPrice: 799, category: 'Beauty', emoji: '✨', rating: 4.7 },
  { id: 3, name: 'Roadster Cotton T-Shirt', price: 499, originalPrice: 999, category: 'Apparel', emoji: '👕', rating: 4.3 },
  { id: 4, name: 'HRX Running Shoes', price: 1899, originalPrice: 2999, category: 'Sports', emoji: '👟', rating: 4.6 },
  { id: 5, name: 'Wildcraft Travel Backpack', price: 1299, originalPrice: 2199, category: 'Sports', emoji: '🎒', rating: 4.4 },
  { id: 6, name: 'Lakme Lipstick Crimson', price: 349, originalPrice: 499, category: 'Beauty', emoji: '💄', rating: 4.5 },
  { id: 7, name: 'Mivi Wireless Earbuds', price: 1499, originalPrice: 2499, category: 'Electronics', emoji: '🎧', rating: 4.6 },
  { id: 8, name: 'Puma Cotton Hoodie', price: 1799, originalPrice: 2999, category: 'Apparel', emoji: '🧥', rating: 4.4 },
];

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-soft sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="text-2xl">🛍️</div>
            <div className="font-bold text-xl text-gray-800">
              QuickShop <span className="text-primary">AI</span>
            </div>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm text-gray-600">
            <a href="#" className="hover:text-primary transition">Home</a>
            <a href="#" className="hover:text-primary transition">Products</a>
            <a href="#" className="hover:text-primary transition">Categories</a>
            <a href="#" className="hover:text-primary transition">About</a>
          </nav>
          <div className="flex items-center gap-3">
            <button className="text-gray-600 hover:text-primary p-2" aria-label="Search">
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            <button className="text-gray-600 hover:text-primary p-2 relative" aria-label="Cart">
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span className="absolute -top-1 -right-1 bg-accent text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-bold">3</span>
            </button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="bg-gradient-to-br from-primary to-primary-dark text-white py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Smart Shopping, <span className="text-yellow-300">Powered by AI</span>
          </h1>
          <p className="text-lg opacity-95 mb-6 max-w-2xl mx-auto">
            Ask our AI assistant anything — about products, prices, orders, or policies.
            Get instant answers from our database and documents.
          </p>
          <div className="flex flex-wrap justify-center gap-3 text-sm">
            <span className="bg-white/20 backdrop-blur px-4 py-2 rounded-full">⚡ Real-time inventory</span>
            <span className="bg-white/20 backdrop-blur px-4 py-2 rounded-full">📦 25,000+ pin codes</span>
            <span className="bg-white/20 backdrop-blur px-4 py-2 rounded-full">🤖 24/7 AI Support</span>
          </div>
        </div>
      </section>

      {/* AI Banner */}
      <section className="max-w-7xl mx-auto px-4 py-6">
        <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-4 flex items-center gap-3">
          <div className="text-2xl">💡</div>
          <div className="flex-1 text-sm text-gray-700">
            <span className="font-semibold">Try the AI Assistant</span> (bottom-right corner) — ask "What's your return policy?" or "How many orders are pending?" — it queries our live PostgreSQL database AND policy PDFs in real-time.
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-end justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Featured Products</h2>
            <p className="text-sm text-gray-500 mt-1">Top picks from our catalog of 100+ items</p>
          </div>
          <a href="#" className="text-sm text-primary hover:underline">View all →</a>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {featuredProducts.map((p) => {
            const discount = Math.round(((p.originalPrice - p.price) / p.originalPrice) * 100);
            return (
              <div key={p.id} className="bg-white rounded-xl shadow-soft hover:shadow-medium transition cursor-pointer overflow-hidden group">
                <div className="aspect-square bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center text-6xl group-hover:scale-105 transition">
                  {p.emoji}
                </div>
                <div className="p-3">
                  <div className="text-[10px] text-primary font-medium uppercase mb-1">{p.category}</div>
                  <div className="text-sm font-medium text-gray-800 line-clamp-2 mb-2 min-h-[40px]">{p.name}</div>
                  <div className="flex items-center gap-1 mb-2">
                    <span className="text-yellow-500 text-xs">★</span>
                    <span className="text-xs text-gray-600">{p.rating}</span>
                  </div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-base font-bold text-gray-900">₹{p.price}</span>
                    <span className="text-xs text-gray-400 line-through">₹{p.originalPrice}</span>
                    <span className="text-xs text-green-600 font-medium">{discount}% off</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Stats */}
      <section className="bg-white border-t border-gray-200 py-12 mt-8">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <div className="text-3xl font-bold text-primary">100+</div>
            <div className="text-sm text-gray-600 mt-1">Products in DB</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary">200+</div>
            <div className="text-sm text-gray-600 mt-1">Customers</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary">1,000+</div>
            <div className="text-sm text-gray-600 mt-1">Orders Processed</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary">24/7</div>
            <div className="text-sm text-gray-600 mt-1">AI Support</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-4">
        <div className="max-w-7xl mx-auto text-center text-sm">
          <div className="font-bold text-white text-lg mb-2">🛍️ QuickShop AI</div>
          <div>Demo project · Built with React, FastAPI, Cloud SQL, Vertex AI Gemini, ChromaDB</div>
          <div className="mt-2 text-xs">© 2026 QuickShop AI · Showcase project for AI-powered e-commerce</div>
        </div>
      </footer>

      {/* The AI Chat Widget */}
      <ChatWidget />
    </div>
  );
}

export default App;

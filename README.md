# 🛍️ QuickShop AI

> **An AI-powered e-commerce assistant that answers questions from both structured databases AND unstructured documents — in one seamless conversation.**

[![GCP](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Cloud Run](https://img.shields.io/badge/Cloud%20Run-Deployed-brightgreen)](https://cloud.google.com/run)

---

## 🎯 What Problem It Solves

Traditional e-commerce chatbots can answer EITHER:
- 📚 **Policy questions** ("What's your return policy?") — via documents/FAQs
- 🗄️ **Data questions** ("How many orders shipped last week?") — via SQL queries

**QuickShop AI does BOTH in one conversation** — automatically deciding which approach to use, even combining both for hybrid questions.

This solves a real users' pain point: e-commerce clients want a single AI assistant that handles both customer policy queries AND business intelligence — without juggling two systems.

---

## 🌐 Live Demo

**👉 [Try it live](https://quickshop-ui-218990051802.asia-south1.run.app)**

**Sample queries to try:**

| Question | What Happens |
|----------|--------------|
| `What is your return policy?` | RAG searches policy PDFs → cites sources |
| `How many customers in Mumbai?` | NL2SQL generates SQL → runs on Cloud SQL |
| `What's your shipping policy and how many pending orders?` | Hybrid — combines both |

---

## 🏗️ Architecture
### Query Flow

1. **User asks a question** via React chat widget
2. **Router (Gemini)** classifies intent: `rag` | `sql` | `both`
3. **RAG path:** Vector search on ChromaDB → retrieve top-3 PDF chunks
4. **SQL path:** Gemini generates safe SQL → executes on Cloud SQL → returns rows
5. **Synthesizer (Gemini)** combines context → produces final answer
6. **Response includes:** answer + source PDFs + generated SQL (transparency)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **LLM** | Google Vertex AI — Gemini 2.5 Flash |
| **Embeddings** | Vertex AI `text-embedding-004` |
| **Vector DB** | ChromaDB (in-memory, cosine similarity) |
| **Structured DB** | Cloud SQL — PostgreSQL 15 |
| **Document Store** | Google Cloud Storage |
| **Deployment** | Cloud Run (serverless, auto-scaling) |
| **Container** | Docker (multi-stage builds) |
| **Auth** | GCP Service Accounts + IAM (least-privilege) |
| **CI/CD** | Cloud Build (source-based deploys) |

---

## 📊 Sample Data

The demo uses realistic Indian e-commerce data:

| Table | Rows | Sample |
|-------|------|--------|
| `customers` | 200 | Names, cities (Mumbai, Bangalore, Delhi…), tiers |
| `products` | 100 | Apparel, Electronics, Beauty, Sports — Indian brands |
| `inventory` | 200+ | Stock levels across 5 warehouses |
| `orders` | 1,000 | Order history with status, payment, dates |

Plus 3 policy PDFs (Return Policy, Shipping Guide, Product FAQ) for the RAG side.

---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- A GCP project with: Vertex AI, Cloud SQL, Cloud Storage enabled
- Cloud SQL PostgreSQL instance

### Backend setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "DB_PASSWORD=your_db_password" > .env

# Run locally
python3 main.py
# Server starts on http://localhost:8080
```

### Frontend setup

```bash
cd frontend
npm install

# Point to local or live backend
echo "VITE_API_URL=http://localhost:8080" > .env.local

npm run dev
# UI starts on http://localhost:5173
```

---

## ☁️ Deploy to Cloud Run

```bash
# Backend
cd backend
gcloud run deploy quickshop-api --source . \
  --region asia-south1 \
  --add-cloudsql-instances PROJECT:REGION:INSTANCE \
  --set-env-vars "DB_PASSWORD=..." \
  --allow-unauthenticated

# Frontend
cd frontend
gcloud run deploy quickshop-ui --source . \
  --region asia-south1 \
  --allow-unauthenticated
```

---

## 📁 Project Structure
---

## 🔐 Security Highlights

- ✅ **Service Account isolation** — backend runs as `quickshop-sa` with only the 4 IAM roles it needs (Vertex AI, Cloud SQL Client, GCS Object Admin, Cloud Run Invoker)
- ✅ **No hardcoded secrets** — `.env` for local dev, Cloud Run env vars for production
- ✅ **SQL injection protection** — read-only safety filter blocks `DELETE`, `UPDATE`, `DROP`, `INSERT`, etc.
- ✅ **Cloud SQL Connector** — encrypted IAM-based DB connection (no exposed IPs)
- ✅ **`.gitignore` rigor** — `.env` and credentials never reach the repo

---

## 💡 What's Next (Phase 2 Roadmap)

- [ ] 🎤 **Voice search** — Cloud Speech-to-Text + Text-to-Speech
- [ ] 🖼️ **Image search** — upload product photo → Gemini Vision finds similar
- [ ] 📊 **Analytics dashboard** — natural-language BI for store owners
- [ ] 🔄 **Streaming responses** — Server-Sent Events for real-time tokens
- [ ] 🌐 **Multilingual** — Hindi, Tamil, Telugu via Gemini's native support

---

## 📜 License

MIT — feel free to use, fork, and adapt.

---

## 👤 Author

**Shakti Srivastava**
- An AI optimist and a researcher
- GitHub: [@shaktisrivastava2020](https://github.com/shaktisrivastava2020)
- Open to freelance AI/ML projects — RAG, NL2SQL, NLP, Deep Learning, GenAI, ConvAI, Speech AI, Vision AI, Agentic, MCP, MLOps products on GCP & AWS

—


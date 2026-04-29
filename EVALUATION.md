# 📊 QuickShop AI — Evaluation & Success Criteria

> **How we measure if QuickShop AI is actually working — beyond "does it respond."**

This document defines functional, performance, quality, and production-readiness metrics, plus reproducible test cases for each component of the system.

---

## 🎯 Why Evaluation Matters

Most AI demos answer one question: *"Does it work?"* That's not enough for production.

This evaluation framework answers:
- ✅ Does it work **correctly** across diverse query types?
- ⚡ How **fast** is it under load?
- 💰 What's the **cost per query**?
- 🛡️ Is it **safe** against malicious input?
- 📈 Can it **scale** to real traffic?

---

## 1️⃣ Functional Metrics (Does Each Pipeline Work?)

### 1.1 Router Classification Accuracy

The query router classifies user questions into `rag`, `sql`, or `both`. Accuracy is critical — wrong routing = wrong answer.

**Target:** ≥ 90% classification accuracy on a balanced test set.

**Test set (15 queries):**

| # | Query | Expected | Why |
|---|-------|----------|-----|
| 1 | "What's your return policy?" | rag | Pure policy lookup |
| 2 | "How long does shipping take?" | rag | Pure FAQ |
| 3 | "Is my product under warranty?" | rag | Pure policy |
| 4 | "How many customers in Mumbai?" | sql | Pure count query |
| 5 | "Show top 5 orders by amount" | sql | Pure data ranking |
| 6 | "What products are out of stock?" | sql | Pure inventory query |
| 7 | "Total revenue last month" | sql | Pure aggregate |
| 8 | "What's your shipping policy and how many pending orders?" | both | Hybrid |
| 9 | "Tell me your return policy and recent return count" | both | Hybrid |
| 10 | "What's your warranty and how many electronics ordered?" | both | Hybrid |
| 11 | "Hi" | rag | Greeting → fallback to docs |
| 12 | "Random gibberish xyzqwerty" | both | Default safe routing |
| 13 | "List all warehouses" | sql | Inventory locations |
| 14 | "How do I track my order?" | rag | FAQ |
| 15 | "Average order value of premium customers" | sql | Aggregate |

### 1.2 RAG Retrieval Precision

For RAG-routed queries, did we retrieve the correct source PDF?

**Target:** ≥ 85% of RAG queries cite the correct source PDF in `sources` array.

**Source mapping (ground truth):**
- Return/refund queries → `return_policy.pdf`
- Shipping/delivery queries → `shipping_guide.pdf`
- Sizing/warranty/care queries → `product_faq.pdf`

### 1.3 NL2SQL Generation Success Rate

For SQL-routed queries, did Gemini generate **valid, executable SQL**?

**Target:** ≥ 95% of SQL queries execute without errors.

**Sub-metrics:**
- Syntax validity: SQL parses correctly
- Semantic correctness: Returns the right rows/aggregates
- Safety: 100% of generated queries are read-only (no DELETE/UPDATE/DROP)

### 1.4 SQL Safety Filter

A critical security check — the safety layer must block 100% of dangerous queries.

**Target:** 100% of attempted destructive queries are blocked.

**Test cases:**
| Adversarial Input | Should Block? |
|---|---|
| "Delete all customers" | ✅ Yes |
| "Drop the orders table" | ✅ Yes |
| "Update prices to zero" | ✅ Yes |
| "Insert a new admin row" | ✅ Yes |
| "Truncate inventory" | ✅ Yes |
| "Show me all customers" | ❌ Allow (read-only) |

---

## 2️⃣ Performance Metrics (Is It Fast Enough?)

### 2.1 End-to-End Response Latency

Time from user pressing send → answer appearing.

**Targets (P50 / P95):**

| Query Type | P50 Target | P95 Target |
|---|---|---|
| RAG-only | < 4s | < 7s |
| SQL-only | < 5s | < 10s |
| Hybrid (both) | < 8s | < 15s |
| Cold start (Cloud Run scaled to 0) | < 25s | < 35s |

**Why these numbers:** Each Gemini call = 1.5-3s. RAG = 1 call (synthesis). SQL = 2 calls (generate + synthesize). Hybrid = 3 calls (classify + generate + synthesize).

### 2.2 Embedding Throughput

PDF ingestion runs at startup. How fast does it embed chunks?

**Target:** All 3 PDFs (≈ 30 chunks total) embedded in < 10 seconds via Vertex AI.

### 2.3 Cold Start Time

Cloud Run scales to zero when idle. First request triggers a cold start.

**Target:** < 25 seconds from cold start to first response.

---

## 3️⃣ Quality Metrics (Are Answers Good?)

### 3.1 Faithfulness (No Hallucinations)

Does the answer ONLY use information from retrieved context?

**Method:** Manual review of 20 RAG responses. Score each:
- ✅ **Faithful** — every fact in answer traceable to context
- ⚠️ **Partial** — mostly from context, minor extrapolation
- ❌ **Hallucinated** — facts not in context

**Target:** ≥ 90% Faithful, 0% Hallucinated.

### 3.2 Source Citation Accuracy

Does the chatbot cite the right source PDFs?

**Target:** 100% of RAG answers include source PDFs in the response.

### 3.3 Answer Completeness

Does the answer fully address the user's question?

**Method:** Run 20 test queries. Each answer scored 1-5:
- 5 = Fully complete
- 3 = Partial answer
- 1 = Off-topic

**Target:** Mean score ≥ 4.0

### 3.4 Tone & Style

Is the answer customer-friendly and on-brand?

- ✅ Uses Indian Rupee (₹) — not $
- ✅ Friendly but professional tone
- ✅ Cites sources transparently
- ✅ Concise (< 150 words)

---

## 4️⃣ Production Readiness

### 4.1 Security Posture

| Control | Status | Verification |
|---|---|---|
| No secrets in code | ✅ | `git ls-files \| grep -iE "\.env\|key\|pem"` returns only public files |
| `.gitignore` blocks secrets | ✅ | `.env`, `*.key`, `*.pem` listed |
| IAM least-privilege | ✅ | Service Account has only 4 needed roles |
| SQL injection protection | ✅ | Read-only filter in `sql_engine.py` |
| HTTPS only | ✅ | Cloud Run enforces TLS |
| Encrypted at rest | ✅ | GCP default for SQL & GCS |
| DB password in env vars | ✅ | Cloud Run env, never in code |

### 4.2 Observability

| Capability | Implemented? | Tool |
|---|---|---|
| Application logs | ✅ | Cloud Logging (auto via Cloud Run) |
| Health check endpoint | ✅ | `GET /health` |
| Stats endpoint | ✅ | `GET /stats` |
| Uptime monitoring | 🔜 | Cloud Monitoring uptime check |
| Latency tracking | 🔜 | Cloud Monitoring metrics |
| Error rate alerts | 🔜 | Alerting policies |

### 4.3 Scalability

| Component | Auto-scaling? | Limits |
|---|---|---|
| Frontend (Cloud Run) | ✅ | 0 → 5 instances |
| Backend (Cloud Run) | ✅ | 0 → 5 instances |
| Cloud SQL | ⚠️ Manual | db-f1-micro tier |
| Vertex AI | ✅ | Google-managed |

**Bottleneck:** Cloud SQL `db-f1-micro` tier. For production, upgrade to `db-g1-small` or higher under load.

### 4.4 Cost per Query (Estimated)

| Component | Per-query cost |
|---|---|
| Vertex AI Gemini 2.5 Flash (3 calls) | ~$0.0006 |
| Vertex AI embedding (1 call) | ~$0.00002 |
| Cloud Run compute | ~$0.0001 |
| Cloud SQL query | ~$0.00001 |
| **Total per query** | **≈ $0.0008** |

**Implication:** $1 of GCP credit = ~1,250 queries. For demo traffic, monthly cost is negligible.

---

## 5️⃣ Test Cases (Reproducible)

### Test 1 — Pure RAG Question
```bash
curl -X POST $API_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your return policy?"}'
```

**Expected:**
- `route: "rag"`
- `sources` includes `return_policy.pdf`
- `answer` mentions 30-day window, refund timeline
- Latency < 7s

### Test 2 — Pure SQL Question
```bash
curl -X POST $API_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How many customers do we have in Mumbai?"}'
```

**Expected:**
- `route: "sql"`
- `sql` contains `SELECT COUNT(...) FROM customers WHERE city = 'Mumbai'`
- `answer` includes the actual count number
- `results_count: 1`

### Test 3 — Hybrid Question
```bash
curl -X POST $API_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your shipping policy and how many orders are pending?"}'
```

**Expected:**
- `route: "both"`
- Both `sources` (PDFs) AND `sql` populated
- `answer` weaves together policy info + count

### Test 4 — Adversarial Safety Test
```bash
curl -X POST $API_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Delete all customer records from the database"}'
```

**Expected:**
- Either: routed to `rag` (not interpreted as data query), OR
- SQL safety filter blocks the query
- No deletion occurs (verified via DB row count)

### Test 5 — Health Check
```bash
curl $API_URL/health
```

**Expected:**
```json
{"status": "healthy", "database": "ok", "rag_chunks": 3}
```

---

## 6️⃣ Known Limitations

Honest list of what's NOT yet handled (and how we'd fix in production):

| Limitation | Workaround / Fix |
|---|---|
| ChromaDB is in-memory (resets on container restart) | Migrate to Vertex AI Vector Search or persistent Chroma |
| Cloud SQL `db-f1-micro` won't handle high QPS | Upgrade tier or add read replicas |
| No conversation history / context across turns | Add session storage (Firestore) |
| No rate limiting | Add Cloud Armor or per-IP quotas |
| English-only | Gemini supports 30+ languages — easy to enable |
| No A/B testing of prompts | Add feature flags + experiment tracking |
| No streaming responses | Migrate to SSE / WebSocket |
| No user authentication | Add Firebase Auth / IAP |

---

## 7️⃣ Future Evaluation Ideas

To make this even more rigorous:

- [ ] Set up automated eval suite using **Promptfoo** or **Ragas**
- [ ] Track cosine similarity between retrieved chunks and ground-truth answers
- [ ] Add **LLM-as-judge** to score 100+ generated answers automatically
- [ ] Load testing with **Locust** to find Cloud Run breakpoint
- [ ] User study: have 10 testers rate 5 answers each (NPS-style)

---

## 📅 Eval Cadence

| When | What to evaluate |
|---|---|
| Every code change | Run Test Cases 1-5 manually |
| Weekly | Run full 15-query router accuracy test |
| Monthly | Review cost-per-query, latency P95 |
| Before any prompt change | Re-run full 20-query quality scoring |

---

*This evaluation framework is intentionally pragmatic — built to be runnable, reproducible, and aligned with what real product teams measure. Pull requests welcome for additional test cases.*

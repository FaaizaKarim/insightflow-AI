<img width="1920" height="832" alt="image" src="https://github.com/user-attachments/assets/839b983b-7d88-4b2b-a40a-567b9d2a3d41" />
<img width="1917" height="648" alt="image" src="https://github.com/user-attachments/assets/3af5b83f-42a6-41e9-82b7-595088041354" />


# InsightFlow AI — Enterprise Data Intelligence Agent

> **One chat interface. Live SQL. ML predictions. Document search. All wired together.**

---

## What Is This Project?

InsightFlow AI is a production-grade **Enterprise Data Intelligence Agent** — a conversational AI system that lets non-technical business users ask natural-language questions and get answers from three distinct data sources simultaneously:

| Path | What Happens |
|---|---|
| **Text-to-SQL** | Agent converts the question into SQL, queries PostgreSQL, returns live rows |
| **ML Prediction** | Agent invokes a trained scikit-learn churn/sales model as a tool |
| **RAG Search** | Agent semantically searches embedded company documents (policies, FAQs) |

The agent (built with **LangGraph**) automatically routes each question to one or more paths, chains them when needed, and returns a coherent natural-language answer with citations.

---

## Why This Project?

Built specifically to demonstrate every requirement in a **Junior AI/ML Engineer** job posting (FocusKPI-style roles):

| Job Requirement | What This Project Does |
|---|---|
| LLM-based chatbot/agent | LangGraph multi-tool agent with Claude/OpenAI |
| SQL / enterprise databases | Real PostgreSQL with Text-to-SQL tool |
| ML models (classification) | scikit-learn churn model exposed as agent tool + REST API |
| Data preprocessing / feature engineering | Full pipeline in `ml/pipeline.py` |
| Vector databases / embeddings | ChromaDB with OpenAI embeddings |
| FastAPI backend | `/chat`, `/predict`, `/query` endpoints |
| LangChain / LangGraph | Agent orchestration layer |
| Docker deployment | Full docker-compose with all services |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)               │
│  Chat UI · Dashboard · ML Results · Document Citations  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP / WebSocket
┌────────────────────▼────────────────────────────────────┐
│                  FASTAPI BACKEND                         │
│  /chat  ·  /predict  ·  /query  ·  /ingest  ·  /health  │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              LANGGRAPH AGENT ROUTER                      │
│                                                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐ │
│  │  SQL Tool    │ │   ML Tool    │ │    RAG Tool      │ │
│  │ Text→SQL     │ │ Churn Pred.  │ │  ChromaDB Search │ │
│  │ PostgreSQL   │ │ scikit-learn │ │  OpenAI Embeds   │ │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘ │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
┌─────────▼────────┐ ┌─────▼──────┐ ┌────────▼──────────┐
│   PostgreSQL DB  │ │  ML Model  │ │    ChromaDB        │
│  (Sales/E-comm   │ │  .pkl file │ │  (Policy docs,     │
│   sample data)   │ │  + scaler  │ │   FAQs, manuals)  │
└──────────────────┘ └────────────┘ └───────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI 0.110+ |
| **Agent Orchestration** | LangGraph 0.1+ |
| **LLM** | Claude 3.5 Sonnet (Anthropic) or GPT-4o |
| **ML** | scikit-learn, pandas, numpy, joblib |
| **Database** | PostgreSQL 15 |
| **Vector Store** | ChromaDB (local) |
| **Embeddings** | OpenAI `text-embedding-3-small` |
| **Frontend** | React 18, Vite, Zustand, TailwindCSS |
| **Auth** | JWT (python-jose) |
| **Container** | Docker + docker-compose |
| **Testing** | pytest, httpx |

---

## Color System

Palette extracted from brand identity:

```
--navy-deep:    #0A2342   (primary dark background)
--navy-mid:     #1A3A6B   (card backgrounds, sidebar)
--blue-core:    #0E6BA8   (primary accent, buttons, links)
--blue-muted:   #6B9AB8   (secondary text, borders)
--blue-light:   #B8D4E3   (highlights, hover states)
--white:        #FFFFFF   (text on dark)
--text-muted:   #A0B4C4   (secondary labels)
```

---

## Project Structure

```
insightflow-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── api/routes/
│   │   │   ├── chat.py              # /chat WebSocket + POST
│   │   │   ├── predict.py           # /predict ML endpoint
│   │   │   ├── query.py             # /query direct SQL endpoint
│   │   │   └── ingest.py            # /ingest document upload
│   │   ├── core/
│   │   │   ├── config.py            # Settings (pydantic-settings)
│   │   │   ├── security.py          # JWT auth
│   │   │   └── logging.py           # Structured logging
│   │   ├── agents/
│   │   │   ├── graph.py             # LangGraph StateGraph definition
│   │   │   ├── nodes.py             # Agent node functions
│   │   │   └── prompts.py           # System prompts
│   │   ├── tools/
│   │   │   ├── sql_tool.py          # Text-to-SQL tool
│   │   │   ├── ml_tool.py           # ML prediction tool
│   │   │   └── rag_tool.py          # RAG search tool
│   │   ├── ml/
│   │   │   ├── pipeline.py          # Training pipeline
│   │   │   ├── predict.py           # Inference
│   │   │   └── models/              # Saved .pkl files
│   │   ├── db/
│   │   │   ├── database.py          # SQLAlchemy async engine
│   │   │   ├── models.py            # ORM models
│   │   │   └── seed.py              # Sample data seeder
│   │   └── schemas/
│   │       ├── chat.py              # Pydantic request/response
│   │       └── predict.py
│   ├── tests/
│   │   ├── test_agent.py
│   │   ├── test_sql_tool.py
│   │   └── test_ml.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/                # Chat window, message bubbles, input
│   │   │   ├── dashboard/           # KPI cards, charts, ML results panel
│   │   │   ├── layout/              # Sidebar, navbar, shell
│   │   │   └── ui/                  # Shared design system components
│   │   ├── pages/
│   │   │   ├── ChatPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   └── LoginPage.jsx
│   │   ├── store/                   # Zustand global state
│   │   ├── services/                # API client (axios)
│   │   └── styles/                  # Tailwind + CSS vars
│   ├── Dockerfile
│   └── package.json
├── docs/
│   └── sample_policies/             # RAG source documents
├── scripts/
│   ├── seed_db.py
│   └── train_model.py
├── docker-compose.yml
└── .env.example
```

---

## Setup & Run

### Prerequisites
- Docker + Docker Compose
- An Anthropic API key (`ANTHROPIC_API_KEY`) **or** OpenAI key
- (Optional) OpenAI key for embeddings (`OPENAI_API_KEY`)

### 1 — Clone and configure
```bash
git clone https://github.com/yourname/insightflow-ai
cd insightflow-ai
cp .env.example .env
# Edit .env and add your API keys
```

### 2 — Start everything
```bash
docker-compose up --build
```

This spins up:
- PostgreSQL on port 5432
- ChromaDB on port 8001
- FastAPI backend on port 8000
- React frontend on port 3000

### 3 — Seed data and train the model
```bash
docker-compose exec backend python scripts/seed_db.py
docker-compose exec backend python scripts/train_model.py
```

### 4 — Open the app
Navigate to **http://localhost:3000**

---

## Example Queries

```
"Which customers are most likely to churn next month?"
→ Agent chains SQL (pull customer features) + ML (run churn prediction)

"What is our refund policy for enterprise clients?"
→ Agent uses RAG to search policy documents and cite the relevant clause

"Show me revenue by region for Q1 2024 and flag underperformers"
→ Agent converts to SQL, runs query, returns table + analysis

"Predict churn for customer ID 4821 and summarize their history"
→ Agent fetches customer data via SQL, passes features to ML model, returns prediction + context
```

---

## Key Engineering Decisions

1. **LangGraph over plain LangChain**: stateful graph lets us add memory, human-in-the-loop approval, and retry logic cleanly.
2. **pgvector vs ChromaDB**: ChromaDB chosen for zero-dependency local dev; pgvector branch available for production (keeps stack to one DB).
3. **Async FastAPI throughout**: all DB calls use `asyncpg`; agent runs in a background task with SSE streaming to frontend.
4. **ML model as a tool, not a service**: scikit-learn model is loaded once at startup and called synchronously inside the tool — avoids an extra microservice for V1.
5. **Text-to-SQL safety**: query is validated against a whitelist of allowed tables; SELECT-only enforced; column names are injected from schema introspection to prevent hallucination.

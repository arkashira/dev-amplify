# TECH_SPEC.md – dev‑amplify

---

## 1. Overview

**dev‑amplify** is an Axentx product that delivers a developer‑first platform for code‑generation, refactoring, and project‑scaffolding.  
It exposes a set of REST/GraphQL APIs that accept natural‑language prompts or code snippets, run them through a fine‑tuned LLM (vLLM + SGLang), and return actionable code, documentation, or CI/CD pipelines. The platform is designed to be plug‑in‑ready for IDEs, CI systems, and low‑code builders.

---

## 2. Architecture

```
┌───────────────────────┐
│  Client (IDE, CLI, UI)│
└─────────────┬─────────┘
              │
              ▼
┌───────────────────────┐
│  API Gateway (FastAPI)│
└───────┬───────┬───────┘
        │       │
        ▼       ▼
┌───────────────┐ ┌───────────────────────┐
│ Auth Service  │ │  Request Router        │
└───────┬───────┘ └───────┬───────┬───────┘
        │                 │       │
        ▼                 ▼       ▼
┌───────────────────────┐ ┌───────────────────────┐
│  LLM Inference (vLLM) │ │  Post‑Processing (SGLang)│
└───────┬───────┬───────┘ └───────┬───────┬───────┘
        │       │               │       │
        ▼       ▼               ▼       ▼
┌───────────────────────┐ ┌───────────────────────┐
│  Data Store (PostgreSQL│ │  Cache (Redis)         │
│   + pgvector)          │ │  (query‑history)       │
└───────┬───────┬───────┘ └───────┬───────┬───────┘
        │       │               │       │
        ▼       ▼               ▼       ▼
┌───────────────────────┐ ┌───────────────────────┐
│  Metrics & Logging (Prometheus/ELK)│ │  Deployment (K8s)     │
└───────────────────────┘ └───────────────────────┘
```

* **API Gateway** – FastAPI + Uvicorn, TLS termination, rate‑limiting.  
* **Auth Service** – OAuth2/JWT, integration with Axentx SSO.  
* **Request Router** – Dispatches to LLM or Post‑Processing based on intent.  
* **LLM Inference** – vLLM serving a 13B Llama‑2 fine‑tuned on `auto`, `instr‑resp`, `messages`, and `query‑resp` datasets.  
* **Post‑Processing** – SGLang for structured code generation, syntax validation, and diff creation.  
* **Data Store** – PostgreSQL 15 + pgvector for semantic search of past prompts.  
* **Cache** – Redis 7 for session state and hot prompts.  
* **Metrics** – Prometheus + Grafana dashboards.  
* **Logging** – ELK stack with structured JSON logs.  
* **Deployment** – Helm charts on a managed Kubernetes cluster (GKE/Azure AKS).  

---

## 3. Components

| Component | Responsibility | Tech |
|-----------|----------------|------|
| **Client SDK** | Language‑agnostic wrapper for API calls | Python, TypeScript |
| **Auth Service** | Token issuance, validation, user‑role mapping | FastAPI, Authlib |
| **Request Router** | Intent detection, routing | FastAPI, Pydantic |
| **LLM Service** | Text generation, code synthesis | vLLM, CUDA 12, NVIDIA A100 |
| **Post‑Processing Service** | Syntax validation, diff generation, documentation extraction | SGLang, Black, isort |
| **Persistence Layer** | Prompt history, user metadata | PostgreSQL + pgvector |
| **Cache Layer** | Session cache, hot prompt cache | Redis |
| **Metrics & Logging** | Observability | Prometheus, Grafana, ELK |
| **Deployment** | CI/CD, Helm, K8s manifests | GitHub Actions, Helm, ArgoCD |

---

## 4. Data Model

```sql
-- users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  role TEXT NOT NULL, -- 'developer', 'admin', etc.
  created_at TIMESTAMP DEFAULT now()
);

-- prompts
CREATE TABLE prompts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  intent TEXT NOT NULL, -- e.g., 'refactor', 'generate', 'docs'
  raw_input TEXT NOT NULL,
  vector VECTOR(1536), -- pgvector embedding
  created_at TIMESTAMP DEFAULT now()
);

-- responses
CREATE TABLE responses (
  id UUID PRIMARY KEY,
  prompt_id UUID REFERENCES prompts(id),
  output TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT now()
);
```

* `vector` column uses `pgvector` for similarity search (e.g., retrieving similar past prompts).  
* `metadata` stores LLM parameters, token counts, and post‑processing flags.

---

## 5. Key APIs / Interfaces

### 5.1 REST Endpoints (FastAPI)

| Method | Path | Description | Request | Response |
|--------|------|-------------|---------|----------|
| POST | `/v1/prompt` | Submit a prompt for processing | `PromptRequest` | `PromptResponse` |
| GET | `/v1/prompt/{id}` | Retrieve a past prompt & response | — | `PromptDetail` |
| GET | `/v1/search` | Semantic search over past prompts | `q: str, limit: int` | `SearchResult[]` |

#### Request/Response Schemas

```json
// PromptRequest
{
  "intent": "refactor",
  "raw_input": "def foo(x): return x*2",
  "options": { "language": "python", "style": "black" }
}

// PromptResponse
{
  "prompt_id": "uuid",
  "status": "processing",
  "estimated_time_ms": 1200
}

// PromptDetail
{
  "prompt_id": "uuid",
  "intent": "refactor",
  "raw_input": "...",
  "response": {
    "output": "def foo(x): return x * 2",
    "diff": "diff --git a/foo.py b/foo.py\n@@ ..."
  },
  "metadata": { "tokens": 42, "model": "llama-2-13b" }
}
```

### 5.2 GraphQL (Optional)

```graphql
type Prompt {
  id: ID!
  intent: String!
  rawInput: String!
  response: Response
}

type Response {
  output: String!
  diff: String
  metadata: JSON
}

type Query {
  prompt(id: ID!): Prompt
  search(q: String!, limit: Int!): [Prompt!]!
}
```

---

## 6. Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **API** | FastAPI, Uvicorn | Async, type‑safe, low‑latency |
| **Auth** | OAuth2/JWT, Authlib | Standard, secure |
| **LLM** | vLLM (CUDA 12) | Production‑grade inference |
| **Post‑Processing** | SGLang, Black, isort | Structured generation & formatting |
| **DB** | PostgreSQL 15 + pgvector | Relational + vector search |
| **Cache** | Redis 7 | Session & hot data |
| **Observability** | Prometheus, Grafana, ELK | Metrics, logs, traces |
| **Deployment** | Helm, K8s, ArgoCD | GitOps, scalability |
| **CI/CD** | GitHub Actions | Automated tests, linting, image build |
| **Container Runtime** | Docker, BuildKit | Reproducible builds |
| **Language SDKs** | Python 3.12, TypeScript 5.0 | Client libraries |

---

## 7. Dependencies

| Category | Package | Version |
|----------|---------|---------|
| **Python** | fastapi | 0.111.0 |
|          | uvicorn | 0.30.0 |
|          | pydantic | 2.8.2 |
|          | authlib | 1.3.1 |
|          | vllm | 0.5.3 |
|          | sglang | 0.1.0 |
|          | psycopg2-binary | 2.9.9 |
|          | redis | 5.0.1 |
|          | python-dotenv | 1.0.1 |
| **Node** | axios | 1.7.2 |
| **Helm** | chart | 3.15.0 |
| **K8s** | kubectl | 1.30.0 |

All dependencies are pinned in `pyproject.toml` / `package.json` and are installed via `poetry` / `npm ci`.

---

## 8. Deployment

### 8.1 Kubernetes Manifest

* **Namespace**: `dev-amplify`
* **Deployments**:
  * `api-gateway` (replicas 3)
  * `auth-service` (replicas 2)
  * `llm-service` (replicas 1, GPU node selector)
  * `postproc-service` (replicas 2)
* **StatefulSets**:
  * `postgresql` (primary + replica)
  * `redis` (replica set)
* **Ingress**: NGINX Ingress Controller with TLS via cert‑manager.
* **Service Mesh**: Istio for traffic shaping and mTLS.
* **Autoscaling**: Horizontal Pod Autoscaler on CPU & memory thresholds.

### 8.2 CI/CD Pipeline

1. **Lint** – flake8, black, eslint.  
2. **Unit Tests** – pytest, jest.  
3. **Build** – Docker buildx, multi‑arch.  
4. **Push** – Docker Hub / ECR.  
5. **Deploy** – Helm upgrade via ArgoCD.  
6. **Smoke Test** – API health check.  

All pipelines are stored under `.github/workflows/`.

---

## 9. Security & Compliance

* **Data Encryption** – TLS 1.3 for all traffic, AES‑256 at rest in PostgreSQL.  
* **Access Control** – RBAC via JWT scopes.  
* **Audit Logging** – All API calls logged with user ID, IP, and timestamp.  
* **GDPR** – Data retention policy: prompts older than 12 months are anonymized and purged.  

---

## 10. Future Enhancements

| Feature | Priority | Notes |
|---------|----------|-------|
| Multi‑model support (e.g., GPT‑4o) | High | Add model selector in API |
| Real‑time collaboration (WebSocket) | Medium | For pair‑programming sessions |
| Plugin SDK | Medium | Allow third‑party extensions |
| Advanced analytics dashboard | Low | Usage, token consumption, churn |

---

### 10.1 Contact & Maintenance

* **Lead Engineer**: Jane Doe – `jane@axentx.com`  
* **Repository**: `arkashira/dev-amplify`  
* **Issue Tracker**: GitHub Issues – label `tech-spec` for discussion.  

---

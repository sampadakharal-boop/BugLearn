# ReconForge AI Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client (Browser)                             │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │    nginx (80)   │
                    │  Reverse Proxy  │
                    └───────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
      ┌───────▼──────┐ ┌───▼──────┐ ┌───▼────┐
      │   Frontend    │ │  Backend  │ │ Static │
      │  Next.js 14   │ │ FastAPI   │ │ Files  │
      │  React 18     │ │ Python    │ │        │
      │  TailwindCSS  │ │ REST API  │ │        │
      └───────────────┘ └─────┬─────┘ └────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
      ┌───────▼─────┐ ┌──────▼──────┐ ┌──────▼──────┐
      │  PostgreSQL  │ │    Redis    │ │   Celery    │
      │   Primary DB │ │ Cache/Queue │ │   Workers   │
      └─────────────┘ └─────────────┘ └─────────────┘
```

## Component Flow

```
Request Flow:
  Browser → nginx → Next.js (SSR/CSR) → API calls → FastAPI → Database/Redis

Scan Flow:
  User submits scan → FastAPI creates Scan record → Celery task queued
  → Celery worker picks up task → Runs recon modules sequentially
  → Updates scan progress in DB → Builds attack surface graph
  → Scan complete → User notified

AI Flow:
  User requests AI explanation → FastAPI → OpenAI API (or fallback)
  → Response formatted → Returned to frontend
```

## Data Model

```
User (1) ──< (N) Target (1) ──< (N) Scan (1) ──< (N) ScanFinding
                                                      │
                                                      └──(N) Finding

Target (1) ──< (N) AttackSurfaceNode
AttackSurfaceNode (N) ──< (N) AttackSurfaceEdge

User (1) ──< (N) UserMission (N) >── (1) Mission
User (1) ──< (N) UserAchievement (N) >── (1) Achievement
User (1) ──< (N) Notification
```

## Technology Decisions

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Backend Framework | FastAPI | Async-first, automatic OpenAPI docs, Pydantic validation |
| Database | PostgreSQL | Reliable, ACID-compliant, JSON support |
| ORM | SQLAlchemy 2.0 | Async support, mature, migration-friendly |
| Task Queue | Celery + Redis | Distributed task processing, scheduling |
| Frontend | Next.js 14 | SSR/SSG, React, file-based routing |
| Styling | TailwindCSS | Utility-first, fast development |
| AI Integration | OpenAI GPT-4 | State-of-the-art, with fallback system |
| Container | Docker + Compose | Reproducible, scalable deployment |
| CI/CD | GitHub Actions | Native integration, free for public repos |

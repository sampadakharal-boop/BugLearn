# BugLearn — ReconForge Learning System

> The world's first AI-driven Bug Bounty Learning, Voice Certification, and Progression-Locked Cybersecurity Academy.

## Overview

BugLearn is a structured, level-based cybersecurity education platform where users learn bug bounty hunting step by step. Each level must be completed by passing an AI Voice Interview before the next level unlocks.

### 7 Levels of Curriculum

| Level | Topic | Task |
|-------|-------|------|
| 1 | Web & Internet Foundations | Identify parts of a URL |
| 2 | HTTP Deep Dive | Login request analysis |
| 3 | Web Architecture | Map web app flow |
| 4 | Passive Recon Concepts | OSINT research plan |
| 5 | Authentication & Sessions | Session hijacking case study |
| 6 | Vulnerability Fundamentals | Identify vulnerability types |
| 7 | Advanced Bug Bounty Concepts | Bug bounty report analysis |

## Tech Stack

- **Backend**: Python FastAPI + SQLAlchemy + SQLite
- **Frontend**: Next.js 14 + React + Tailwind CSS
- **Auth**: JWT (python-jose) + bcrypt
- **Audio**: Web Speech API (browser-based voice recording)

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
npm install
npm run dev
```

Visit `http://localhost:3000` to start learning.

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/me` | Get current user |
| GET | `/api/v1/levels/current` | Get current level content |
| GET | `/api/v1/levels/` | Get all level progress |
| GET | `/api/v1/levels/{id}` | Get specific level |
| POST | `/api/v1/levels/{id}/complete` | Mark level complete |
| POST | `/api/v1/interview/submit` | Submit interview for scoring |
| GET | `/api/v1/interview/history` | Get interview attempts |
| GET | `/api/v1/interview/prompt/{level}` | Get interview prompt |

| GET | `/api/v1/leaderboard` | Get leaderboard |

## System Rules

- No user can skip levels
- Interview is mandatory for unlocking next level
- Only the current level is visible (future levels locked)
- Passing interview score: 86/100 minimum
- Scoring breakdown: 40% technical, 25% completeness, 20% clarity, 15% real-world
- All progress stored in database


## Database Schema

- **users**: id, name, email, password_hash, current_level, xp_points, created_at
- **level_progress**: id, user_id, level_number, status (locked/in_progress/completed), interview_score, last_attempt_date
- **interview_attempts**: id, user_id, level_number, audio_transcript, score, passed, feedback, created_at
- **leaderboard**: user_id, xp_points, level_reached, rank

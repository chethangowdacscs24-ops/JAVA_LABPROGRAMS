# ASYLUM — Help requests & NGO discovery

**Hackathon-winning MVP.** Refugees and asylum seekers post help requests; NGOs discover and respond. Location-based, no authentication.

---

## Features

- **Refugees:** Submit help requests (location, type, language, optional contact). Find NGOs by city.
- **NGOs:** Browse and filter help requests. Register your organization. Contact people via provided details.
- **Demo:** One-click seed data for showcases.

## Tech stack

| Layer      | Tech                |
|-----------|----------------------|
| Frontend  | SvelteKit            |
| Backend   | FastAPI (Python)     |
| Database  | SQLite (default) or PostgreSQL |
| Deploy    | Docker Compose       |

---

## Quick start (local) — one server, no Node needed

The API also serves the app UI. You only need Python.

1. **Start the server** (uses port **8001** so it won't conflict with other apps on 8000):
   - Double‑click **`START_SERVER.bat`** in the project folder, or
   - In a terminal:  
     `cd c:\Users\Student.CCPLAB-51.000\Desktop\ASYLUM`  
     `pip install -r api/requirements.txt`  
     `python -m uvicorn api.main:app --host 127.0.0.1 --port 8001`
2. **Open in your browser:** **http://127.0.0.1:8001**

If you see **ERR_CONNECTION_REFUSED**: the server is not running. Run step 1 again.

- App: **http://127.0.0.1:8001**
- API docs: **http://127.0.0.1:8001/docs**

### Frontend (SvelteKit)

```bash
npm install
npm run dev
```

- App: **http://localhost:5173**

Use **Load demo data** on the home page to seed sample requests and NGOs.

---

## Run with Docker (full stack)

Requires [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

```bash
docker compose up --build
```

- **Web:** http://localhost:5173  
- **API:** http://localhost:8000  
- **PostgreSQL:** localhost:5432 (user `asylum`, password `asylum`, db `asylum`)

Frontend talks to the API at `http://localhost:8000` (from the browser).

---

## API overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/help-request` | Create help request |
| GET | `/help-requests` | List (optional: `?location=Berlin&help_type=housing`) |
| GET | `/help-requests/{id}` | Get one request |
| POST | `/ngo` | Register NGO |
| GET | `/ngos` | List (optional: `?location=Berlin`) |
| GET | `/ngos/nearby?location=Berlin` | NGOs by location |
| GET | `/stats` | Counts: `help_requests`, `ngos` |
| POST | `/seed` | Insert demo data (only if DB empty) |

---

## Project layout

```
ASYLUM/
├── api/
│   ├── main.py          # FastAPI app, SQLite + Postgres
│   ├── requirements.txt
│   └── Dockerfile
├── web/
│   └── Dockerfile
├── src/
│   ├── routes/          # Home, submit, requests, ngos, ngos/register
│   └── lib/api/         # API client
├── scripts/
│   └── init_db.sql      # PostgreSQL schema
├── docker-compose.yml
└── README.md
```

---

## Environment

| Variable       | Default              | Description |
|----------------|----------------------|-------------|
| `DATABASE_URL` | `sqlite:///./asylum.db` | DB connection (use `postgresql://...` for Postgres) |
| `VITE_API_URL` | `http://localhost:8000`  | Backend URL for the frontend (Docker: keep for browser) |

---

*Built for the hackathon. No auth, no roles — keep it simple.*

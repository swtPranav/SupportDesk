# SupportDesk

SupportDesk is a full-stack customer support ticketing CRM. Customers can submit support requests without an account, while approved staff manage tickets, add internal notes, assign ownership, and track workload through a protected dashboard.

## Highlights

- Public support form at `/support` - no customer account required.
- Unique ticket IDs and timestamps for every request.
- Protected staff workspace for ticket search, filtering, pagination, and updates.
- Ticket detail view with status, priority, description, assignment, and internal notes.
- Administrator-controlled employee onboarding and sign-in approval.
- Live dashboard metrics for ticket status, priority, assignments, and active agents.
- PostgreSQL-ready backend with SQLite support for local development.

## Architecture

| Layer | Technology |
| --- | --- |
| Frontend | React, Vite, React Router, Axios, Lucide |
| Backend | Python, FastAPI, SQLAlchemy, Uvicorn |
| Database | PostgreSQL in production; SQLite locally |
| Authentication | Bearer access tokens with role-based authorization |
| Deployment | Vercel frontend and Railway backend |

## User roles

| User | Access |
| --- | --- |
| Customer | Submits a support request through `/support`; no sign-in needed. |
| Agent | Can sign in only after an administrator approves access; can manage tickets and notes. |
| Administrator | The deployment-configured owner account. It manages employees, approves/revokes access, and assigns tickets. |

The `ADMIN_EMAIL` and `ADMIN_PASSWORD` environment variables define the sole administrator account. On backend startup, the configured administrator is restored and any other administrator roles are demoted to agents. Change `ADMIN_PASSWORD` in Railway and redeploy to reset the administrator password.

## Project structure

```text
SupportDesk/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy entities
│   │   ├── routers/       # Auth, tickets, notes, users, dashboard
│   │   ├── schemas/       # Request and response validation
│   │   ├── main.py        # FastAPI application and startup admin bootstrap
│   │   └── database.py    # SQLite/PostgreSQL connection setup
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── context/
    │   ├── pages/
    │   └── services/
    ├── .env.example
    └── vercel.json
```

## Run locally

### Prerequisites

- Python 3.12+
- Node.js 20+

### 1. Start the API

```powershell
cd backend
Copy-Item .env.example .env
```

Edit `backend/.env` and set at least a strong `SECRET_KEY`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API starts at `http://127.0.0.1:8000`; interactive API documentation is available at `/docs`.

### 2. Start the frontend

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

The frontend starts at `http://127.0.0.1:5173`.

## Environment variables

### Backend

| Variable | Required | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | Yes in production | Database connection string. Use Railway PostgreSQL's injected URL in production. |
| `SECRET_KEY` | Yes | Long random secret used to sign access tokens. |
| `ADMIN_NAME` | Yes | Display name for the sole administrator. |
| `ADMIN_EMAIL` | Yes | Administrator login email. |
| `ADMIN_PASSWORD` | Yes | Administrator password; changing it and restarting resets access. |
| `FRONTEND_ORIGINS` | Yes in production | Comma-separated frontend URLs permitted by CORS. |

### Frontend

| Variable | Required | Purpose |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Yes in production | Public Railway API URL, without a trailing slash. |

Never commit `.env` files or real credentials.

## API overview

| Method | Endpoint | Access | Purpose |
| --- | --- | --- | --- |
| `POST` | `/api/tickets/public` | Public | Create an unassigned customer ticket. |
| `POST` | `/api/auth/login` | Public | Staff sign-in. |
| `GET` | `/api/dashboard/stats` | Staff | Dashboard statistics. |
| `GET`, `POST` | `/api/tickets` | Staff | List/search tickets or create one internally. |
| `GET`, `PUT` | `/api/tickets/{ticket_id}` | Staff | View and update a ticket. |
| `PUT` | `/api/tickets/{ticket_id}/assign` | Admin | Assign or unassign a ticket. |
| `GET`, `POST` | `/api/tickets/{ticket_id}/notes` | Staff | View and add internal notes. |
| `GET`, `POST`, `PATCH` | `/api/users` | Admin | Manage employees and approve/revoke staff access. |

Full OpenAPI documentation is exposed at `https://<api-domain>/docs`.

## Deployment

### Railway - backend

1. Import this repository into Railway and set the service **Root Directory** to `backend`.
2. Deploy from the `main` branch. Railway uses `backend/Dockerfile`.
3. Add a Railway PostgreSQL service and set `DATABASE_URL` on the backend service to its connection URL.
4. Set `SECRET_KEY`, `ADMIN_NAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `FRONTEND_ORIGINS`.
5. Generate a public domain and verify `https://<api-domain>/health` returns `{"status":"healthy"}`.

### Vercel - frontend

1. Import this repository into Vercel and set the **Root Directory** to `frontend`.
2. Select the Vite preset.
3. Set `VITE_API_BASE_URL=https://<api-domain>`.
4. Deploy. The included `vercel.json` supports direct access to client routes such as `/support` and `/tickets/TKT-001`.
5. Update Railway `FRONTEND_ORIGINS` with the exact Vercel URL and redeploy the API.

## Validation

From `frontend`:

```powershell
npm run lint
npm run build
```

Recommended production smoke test:

1. Open `/support` and submit a ticket.
2. Sign in through `/login` as the configured administrator.
3. Find the new ticket, update its status, add a note, and assign it.
4. Add an employee, verify they cannot sign in until approved, then approve them.

## Assessment alignment

This project meets and exceeds the core Support CRM assessment scope:

- Ticket creation with customer details, generated ticket ID, and timestamps.
- Ticket list containing ID, customer, subject, status, and created date.
- Search across customer details, subject, and description; status filtering is included.
- Ticket detail and update flows, including internal notes.
- Full-stack FastAPI + database + React architecture with a responsive UI.
- Production deployment structure, `.env.example` files, `.gitignore`, Docker configuration, and setup documentation.

The public `/support` page is the evaluator-facing customer-entry path. Staff features intentionally require the administrator credentials you configure in Railway.

## License

This repository was created as an assessment project. Add a license before distributing it as an open-source product.

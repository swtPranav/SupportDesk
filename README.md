# SupportDesk CRM

SupportDesk is a FastAPI and React customer-support ticketing application. It provides token-based authentication, a dashboard, ticket lifecycle management, internal notes, and admin user management.

## Run locally

Copy `backend/.env.example` to `backend/.env`, set a real `SECRET_KEY`, and set `ADMIN_EMAIL` and `ADMIN_PASSWORD`. The app creates that admin account the first time it starts. Then start the API from `backend`:

```powershell
uvicorn app.main:app --reload
```

Copy `frontend/.env.example` to `frontend/.env`. Start the web app in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend is served at `http://127.0.0.1:5173` and the API at `http://127.0.0.1:8000`.

Customers do not need an account to create a request. Publish the frontend's `/support` route as the public support URL; it creates an unassigned Open ticket through `POST /api/tickets/public`. Keep `/login` for staff only.

## Main features

- Authenticated, protected dashboard with live ticket statistics.
- Ticket search, filtering, pagination, and creation.
- Public no-account support-request form at `/support`.
- Ticket detail view with editable subject, description, status, and priority.
- Internal ticket notes.
- Admin-only ticket assignment and agent account management.
- Centralized Axios authentication and automatic invalid-token sign-out.

## Verification

From `frontend`, run:

```powershell
npm run lint
npm run build
```

API endpoints are documented interactively at `http://127.0.0.1:8000/docs` while the server is running.

## Deployment handoff

Deploy `backend` as a Docker service on Railway, Render, or a comparable host. Attach persistent storage if you keep SQLite; a managed PostgreSQL database is recommended for a production deployment. Set `DATABASE_URL`, `SECRET_KEY`, `ADMIN_NAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `FRONTEND_ORIGINS` (the frontend's deployed URL) as host environment variables.

### Railway backend

1. Create a Railway service from this GitHub repository and set its **Root Directory** to `backend`. Railway will use `backend/Dockerfile`; do not override its start command.
2. Add a Railway PostgreSQL service and set the backend service's `DATABASE_URL` to the PostgreSQL service's `DATABASE_URL` reference. The backend supports Railway's `postgresql://` URL directly.
3. Set these backend variables: `SECRET_KEY` (a long random value), `ADMIN_NAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `FRONTEND_ORIGINS`. Set `FRONTEND_ORIGINS` to the exact Vercel URL, for example `https://supportdesk.example.vercel.app` (comma-separate multiple URLs if needed).
4. Deploy again, open `https://<your-railway-domain>/health`, and expect `{"status":"healthy"}`. The `argon2-cffi` dependency is required by the password library and is included in `backend/requirements.txt`.

Deploy `frontend` to Vercel as a Vite project with `frontend` as the root directory. Set `VITE_API_BASE_URL` to the deployed backend URL before building. The included `vercel.json` serves the React app correctly for direct links such as `/support` and `/tickets/TKT-001`.

For the assessment, share `/support` as the public customer link and provide the evaluator with the configured admin email and password to demonstrate the staff ticket list, search, status update, and notes.

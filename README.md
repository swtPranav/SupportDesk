# SupportDesk CRM

SupportDesk is a FastAPI and React customer-support ticketing application. It provides token-based authentication, a dashboard, ticket lifecycle management, internal notes, and admin user management.

## Run locally

Start the API from `backend` using the project's Python environment:

```powershell
uvicorn app.main:app --reload
```

Start the web app in a second terminal:

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

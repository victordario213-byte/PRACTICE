# ClubSync

ClubSync — Sports Club Management System

This workspace contains a Flask backend (`/backend`) and a React (Vite) frontend (`/frontend`).

Quick start (development)

1. Backend

- Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

- Configure environment variables (use `backend/.env.example` as a guide). For local development you can set the DB url to a local Postgres instance or use the default development URI configured in `backend/config.py`.

- Initialize database migrations (use Flask-Migrate via Flask CLI):

```bash
# from repo root
export FLASK_APP=main:create_app
export FLASK_ENV=development
cd backend
flask db init   # only the first time
flask db migrate -m "Initial"
flask db upgrade
```

- Seed the database with sample data (optional):

```bash
python3 backend/seed.py
```

- Run the backend:

```bash
python3 backend/main.py
# or
export FLASK_APP=main:create_app
flask run --host=0.0.0.0 --port=5000
```

2. Frontend

- Install dependencies and run dev server:

```bash
cd frontend
npm install
npm run dev
```

- Production build:

```bash
npm run build
npm run preview
```

3. Environment variables

- `backend/.env.example` contains recommended variables for the backend.
- `frontend/.env.example` shows how to set `VITE_API_URL` for local development.

4. Notes

- The backend uses Flask app factory (`main.create_app`) and `extensions.init_extensions` to initialize SQLAlchemy, Migrate, JWT and CORS.
- To run Flask-Migrate (`flask db` commands) ensure `FLASK_APP=main:create_app` is exported in your shell so Flask can find the app factory.
- The frontend uses `VITE_API_URL` (defaults to `http://localhost:5000`) to target the backend API.

If you want, I can now add example Postgres Docker config, CI commands, or wire deploy scripts.

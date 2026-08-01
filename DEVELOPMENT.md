# Development guide

## VS Code quick start

Open this repository as a folder in VS Code. The included `.vscode/tasks.json` provides tasks for the backend, frontend, tests, and Docker Compose.

1. Open **Terminal → Run Task**.
2. Run **Backend: install** once.
3. Start **Backend: run**.
4. Start **Frontend: run** in a second task.
5. Open `http://localhost:5173`.

The API documentation is available at `http://localhost:8000/docs`.

## Verification before review

```powershell
cd backend
python -m pytest -q
cd ..
node --check frontend/assets/app.js
```

Do not commit `.env`, database files, tokens, or private datasets.

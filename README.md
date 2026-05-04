# AI-health-assistant

This project now includes:

- `backend/` for a `FastAPI` API built on top of the existing hospital management modules.
- `frontend/` for a browser-based dashboard using plain HTML, CSS, and JavaScript.
- The original `main.py` Streamlit app is still available.

## Run the backend

```bash
uvicorn backend.app:app --reload
```

Open:

- API root: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:8000/frontend/`

## Existing Streamlit app

```bash
streamlit run main.py
```

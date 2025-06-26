# Streamlit Trading App

Make a copy of `.env.dev` to `.env`.
Run `create_encryption_key.py` and add it to environment variable `PASSWORD_ENCRYPTION_KEY` in your `.env`.

Use the following commands to start up

```bash
    alembic upgrade head
    uv run -- streamlit run 🏠_Home.py
```

Creating migrations
```bash
    alembic revision --autogenerate -m "Add tables"
```

Apply migrations
```bash
    alembic upgrade head
```

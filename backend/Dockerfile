FROM python:3.9-slim

WORKDIR /app

COPY ../requirements .
RUN pip install -r requirements

COPY ../backend .
COPY ../backend/static /app/static


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
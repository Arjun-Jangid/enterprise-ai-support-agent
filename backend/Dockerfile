FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch

RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .

COPY backend ./backend

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
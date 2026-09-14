FROM python:3.11

WORKDIR /app

COPY frontend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .

COPY frontend ./frontend

CMD ["streamlit", "run", "frontend/index.py", "--server.address=0.0.0.0", "--server.port=8501"] 

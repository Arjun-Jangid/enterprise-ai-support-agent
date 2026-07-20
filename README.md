# AI Enterprise Support Agent

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-AI%20Workflow-orange)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Groq](https://img.shields.io/badge/Groq-LLM-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

An enterprise-grade AI support agent powered by Retrieval-Augmented Generation (RAG), LangGraph, and Groq LLM. The application enables authenticated users to upload business documents and interact with them through natural language conversations with source-backed responses.

The application leverages **LangChain**, **LangGraph**, **FastAPI**, **ChromaDB**, **Groq LLM**, and **Docker** to provide accurate, context-aware responses with persistent chat history and source citations.

---

# Project Highlights

- Enterprise RAG Pipeline
- LangGraph Workflow
- Persistent Chat History
- Groq LLM Integration
- ChromaDB Vector Database
- Dockerized Backend & Frontend
- Docker Compose Deployment
- Source Citations

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [LangGraph Workflow](#langgraph-workflow)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)
- [Project Highlights](#project-highlights)
- [Author](#author)

## Features

### Authentication

- JWT-based authentication
- User registration and login

### Document Processing

- Upload PDF, DOCX, and TXT documents
- Automatic text extraction
- SHA-256 based duplicate document detection
- Automatic text chunking
- Document metadata storage

### Retrieval-Augmented Generation (RAG)

- Semantic search using ChromaDB
- SentenceTransformer embeddings
- Context-aware answer generation
- Source citations with similarity scores

### LangGraph Workflow

- State-based workflow orchestration
- Graph-based execution instead of sequential pipelines
- Conditional routing
- State management
- Chat history persistence

### Database

- User management
- Document metadata
- Persistent chat history
- Conversation retrieval

### Frontend

- Streamlit conversational interface
- Document upload
- Source citation display
- Chat history sidebar
- Authentication UI

### DevOps

- Dockerized backend and frontend
- Docker Compose for multi-container orchestration
- Environment variable management using `.env`

---

## System Architecture

```
                        User
                          │
                          ▼
                  Streamlit Frontend
                    (Docker Container)
                          │
                          ▼
                 FastAPI Backend API
                    (Docker Container)
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
 Authentication      LangGraph             SQLite
        │                 │
        ▼                 ▼
  JWT Authentication   RAG Pipeline
                             │
                 ┌───────────┴────────────┐
                 ▼                        ▼
            ChromaDB              Sentence Transformers
                 │
                 ▼
             Groq LLM
```

---

## LangGraph Workflow

```
                    User Question
                          │
                          ▼
                    Router Node
                          │
                          ▼
                  Retrieve Context
                          │
                          ▼
                  Generate Response
                          │
                          ▼
                 Save Chat History
                          │
                          ▼
                    Return Answer
```

---

## Project Structure

```text
AI-Enterprise-Support-Agent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── document/
│   │   ├── graph/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   └── Dockerfile
│
├── frontend/
│   ├── component/
│   ├── pages/
│   ├── utils/
│   ├── index.py
│   └── Dockerfile
│
├── data/
│   ├── chroma_db/
│   └── enterprise.db
│
├── images/
│   ├── login.png
│   ├── signup.png
│   ├── upload.png
│   ├── chat_interface.png
│   └── source_citations.png
│
├── uploads/
│
├── docker-compose.yml
├── requirements.txt
├── config.py
└── README.md
```

---

## Database Schema

### Users

| Column   | Description  |
| -------- | ------------ |
| id       | Primary Key  |
| name     | User name    |
| email    | Unique email |
| password | Password     |

---

### Documents

| Column        | Description       |
| ------------- | ----------------- |
| id            | Primary Key       |
| user_id       | Foreign Key       |
| file_hash     | SHA-256 hash      |
| original_name | Uploaded filename |
| stored_path   | Saved text path   |
| uploaded_at   | Upload timestamp  |

---

### Chat History

| Column      | Description         |
| ----------- | ------------------- |
| id          | Primary Key         |
| user_id     | Foreign Key         |
| document_id | Foreign Key         |
| role        | User / Assistant    |
| message     | Conversation text   |
| sources     | Sources of response |
| created_at  | Timestamp           |

---

## Tech Stack

| Category        | Technologies                  |
| --------------- | ----------------------------- |
| Backend         | FastAPI, SQLAlchemy, Pydantic |
| AI/LLM          | LangChain, LangGraph, Groq    |
| Vector Database | ChromaDB                      |
| Embeddings      | SentenceTransformers          |
| Database        | SQLite                        |
| Frontend        | Streamlit                     |
| DevOps          | Docker, Docker Compose        |

---

## API Endpoints

### Authentication

```
POST /signup
POST /login
```

### Documents

```
POST /upload
```

### Question/Answer

```
POST /ask
```

### Chat

```
GET  /chat-history/{document_id}
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/AI-Enterprise-Support-Agent.git

cd AI-Enterprise-Support-Agent
```

---

### 2. Configure Environment Variables

Create a `.env` file in the project root and add the required environment variables.

```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret_key
DATABASE_URL=your_database_url
```

---

### Run Locally

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Start the Backend

```bash
uvicorn backend.app.main:app --reload
```

#### 3. Start the Frontend

```bash
streamlit run frontend/index.py
```

The application will be available at:

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

---

### Run with Docker

#### Build and Start the Application

```bash
docker compose up --build
```

The application will be available at:

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

To stop the containers:

```bash
docker compose down
```

---

## Screenshots

### Login

![Login](images/login.png)

---

### Signup

![Signup](images/signup.png)

---

### Document Upload

![Document Upload](images/upload.png)

---

### Chat Interface

![Chat Interface](images/chat_interface.png)

---

### Source Citations

![Source Citations](images/source_citations.png)

---

## Future Improvements

- Multi-Agent Workflow
- Hybrid Retrieval (BM25 + Dense Retrieval)
- AWS EC2 Deployment
- GitHub Actions CI/CD
- Kubernetes Deployment
- Monitoring & Logging

---

## Author

**Arjun Jangid**

AI Engineer | Machine Learning | LLM | RAG | LangChain | LangGraph

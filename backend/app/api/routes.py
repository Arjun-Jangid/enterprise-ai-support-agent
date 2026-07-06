import hashlib
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from config import UPLOAD_DIR
from backend.app.db.connection import get_db
from backend.app.models.models import ChatHistory, User, Document
from backend.app.schemas.schemas import SignUpSchema, LoginSchema, AskQuerySchema
from backend.app.utils.auth import create_access_token, get_current_user
from backend.app.document.text_extractor import extract_docx_text, extract_pdf_text, extract_txt_text
from backend.app.document.file_writer import save_text_file
from backend.app.rag.ingestion import ingest_document
from backend.app.rag.history import build_langchain_history
from backend.app.graph.graph import graph


router = APIRouter()

@router.get("/")
def index():    
    return {"message": "Welcome to the AI Enterprise Backend."}


@router.post("/sign-up")
def singup(request: SignUpSchema, db: Session=Depends(get_db)):

    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    try:
        db_user = User(
            name=request.name,
            email=request.email,
            password=request.password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        token = create_access_token(
        {"user_id": db_user.id}
        )

        return {
            "message": "Signup successful",
            "user": {
                "id": db_user.id,
                "name": db_user.name,
                "email": db_user.email
            },
            "access_token": token,
            "token_type": "Bearer",
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if user is None or user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"user_id": user.id}
    )


    return {
       "message": "Login successful",
       "user_id": user.id,
       "access_token": token,
       "token_type": "Bearer"
    }


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user:User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Read file once
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file.")
        
        # Generate hash
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Duplicate check
        doc = (
            db.query(Document)
            .filter(
                Document.user_id == current_user.id,
                Document.file_hash == file_hash,
            )
            .first()
        )

        if doc:
            return {
                "document_id": doc.id,
                "message": "Document already uploaded."
            }

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is missing."
            )
        
        text: str | None = None
        file_type = Path(file.filename).suffix.lower()

        # Extract text
        if file_type == ".pdf":
            text = extract_pdf_text(file_bytes)
        elif file_type == ".txt":
            text = extract_txt_text(file_bytes)
        elif file_type == ".docx":
            text = extract_docx_text(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")


        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted.")
        
        target_file_path = UPLOAD_DIR / f"{file_hash}.txt"

        # Save extracted text
        if not save_text_file(text, target_file_path):
            raise HTTPException(status_code=500, detail="Failed to save text file.")
        

        # Insert DB
        db_doc = Document(
            user_id=current_user.id,
            file_hash=file_hash,
            original_name=file.filename,
            stored_path=str(target_file_path),
            uploaded_at=datetime.now(timezone.utc)
        )

        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)

        # Create embeddings
        ingest_document(
            text=text,
            file_name=file.filename,
            user_id=current_user.id,
            document_id=db_doc.id
            )

    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    return {
        "document_id": db_doc.id,
        "message": "Document uploaded successfully.",
    }


@router.post("/ask")
def ask_query(
    request: AskQuerySchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    try:

        # Verify document
        document = (db.query(Document)
        .filter(Document.id == request.document_id,
                Document.user_id == current_user.id
                )
                .first()
                )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )
        

        # Load previous conversation
        chat_history = (db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id,
                ChatHistory.document_id == request.document_id
                ).order_by(ChatHistory.created_at.asc())
                .all()
                )
        

        # Convert chat history to LangChain messages
        messages = build_langchain_history(chat_history)

        initial_state = {
            "question": request.query,
            "user_id": current_user.id,
            "document_id": request.document_id,
            "chat_history": messages,
            "db": db,
        }

        # Generate answer using LangGraph Workflow
        result = graph.invoke(initial_state)

        return {
            "answer": result["answer"],
            "sources": result["sources"],
        }
    
    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to process your request.",
        )
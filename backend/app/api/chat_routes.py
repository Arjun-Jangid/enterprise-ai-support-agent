
from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.schemas import ChatHistoryRequest
from backend.app.models.models import ChatHistory
from backend.app.db.connection import get_db
from backend.app.models.models import User
from backend.app.utils.auth import get_current_user
from sqlalchemy.orm import Session

from datetime import datetime, timezone

router = APIRouter(prefix="/chat-history")

@router.post("/")
def save_chat_history(
    request: ChatHistoryRequest,
    current_user:User = Depends(get_current_user),
    db:Session = Depends(get_db)
    ):

    if not request:
        raise HTTPException(status_code=400, detail="Empty message.")
    
    # User row
    db_user_mesage = ChatHistory(
        user_id=current_user.id,
        document_id=request.document_id,
        role="user",
        message=request.user_message,
        sources=None,
        created_at=datetime.now(timezone.utc),
    )

    # Assistant row
    db_assistant_mesage = ChatHistory(
        user_id=current_user.id,
        document_id=request.document_id,
        role="assistant",
        message=request.assistant_message,
        sources=request.sources,
        created_at=datetime.now(timezone.utc),
    )
    
    db.add_all([db_user_mesage, db_assistant_mesage])
    db.commit()

    return {
        "message": "messages send successfully"
    }

@router.get("/{document_id}")
def get_chat_history(document_id: int, db:Session = Depends(get_db)):

    if document_id:
        try:
            documents = (
                db.query(ChatHistory)
                .filter(ChatHistory.document_id == document_id)
                .order_by(ChatHistory.created_at.asc())
                .all())
            return {
                "message": "documents get successfully",
                "data": documents
            }
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
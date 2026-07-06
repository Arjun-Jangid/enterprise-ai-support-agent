
from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.schemas import ChatHistoryListResponse
from backend.app.models.models import ChatHistory
from backend.app.db.connection import get_db
from backend.app.utils.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat-history")


@router.get("/{document_id}", response_model=ChatHistoryListResponse)
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
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.connection import get_db
from backend.app.db.models import User, Chat
from backend.app.schemas.schemas import ChatSchema, UserSchema


router = APIRouter()

@router.get("/")
def index():
    return {"message": "Welcome to the API!"}


@router.post("/users")
def create_user(request: UserSchema, db: Session = Depends(get_db)):

    db_user = User(name=request.name, email=request.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
            "status": "success",
            "data": db_user
        }


@router.post("/chats")
def create_chat(request: ChatSchema, db: Session = Depends(get_db)):
    db_chat = Chat(message=request.message)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return {
        "status": "success",
        "data": db_chat
    }



from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from backend.app.db.connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    documents = relationship("Document", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_hash = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="documents")
    chats = relationship("ChatHistory", back_populates="document")


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    role = Column(String, nullable=False)
    message = Column(String, nullable=False)
    sources = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="chats")
    document = relationship("Document", back_populates="chats")

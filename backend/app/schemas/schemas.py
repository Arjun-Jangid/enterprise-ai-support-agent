from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class SignUpSchema(BaseModel):
    name: str = Field(..., description="Name of the user")
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the email")

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the email")

class AskQuerySchema(BaseModel):
    document_id: int = Field(..., description="id of the document")
    query: str = Field(..., description="text of question")

class ChatHistoryRequest(BaseModel):
    document_id: int = Field(..., description="Id of document")
    user_message: str =  Field(..., description="message of user")
    assistant_message: str =  Field(..., description="message of assistant")
    sources: list | None = None

class ChatHistoryResponse(BaseModel):
    role: str
    message: str
    sources: list | None = None
    created_at: datetime

class ChatHistoryListResponse(BaseModel):
    message: str
    data: list[ChatHistoryResponse]
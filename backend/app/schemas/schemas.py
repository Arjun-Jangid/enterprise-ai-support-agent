from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")


class ChatSchema(BaseModel):
    message: str = Field(..., min_length=1, description="The message content")
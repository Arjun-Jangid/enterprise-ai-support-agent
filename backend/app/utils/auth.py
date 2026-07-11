from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.db.connection import get_db
from backend.app.models.models import User
from sqlalchemy.orm import Session

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    payload["exp"] = expire

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]

    except JWTError:
        raise HTTPException(status_code=401, detail="Authentication failed. Please log in again.")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
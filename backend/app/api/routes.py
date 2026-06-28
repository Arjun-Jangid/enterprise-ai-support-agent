from fastapi import APIRouter, Depends, HTTPException, status
from requests import status_codes
from sqlalchemy.orm import Session
from backend.app.db.connection import get_db
from backend.app.db.models import User
from backend.app.schemas.schemas import SignUpSchema, LoginSchema
from backend.app.utils.auth import create_access_token


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
       "access_token": token,
       "token_type": "Bearer"
    }



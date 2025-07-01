from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import crud
from app.db.schemas import user as user_schema
from app.api.v1 import deps
from app.core import security

router = APIRouter(prefix="/auth",tags=["Auhtentication"])

@router.post("/signup",response_model=user_schema.UserResponse,status_code=status.HTTP_201_CREATED)
def singup(user: user_schema.UserCreate,db: Session =Depends(deps.get_db)):
    """Register User"""
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bu email oldin ishlatilgan")
    created_user = crud.create_user(db=db, user=user)
    return created_user

@router.post("/login", response_model=user_schema.Token)
def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in a user and get access and refresh tokens.
    """
    user = crud.get_user_by_email(db, email=form_data.username) # OAuth2 formasi "username" maydonini ishlatadi
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Access va Refresh tokenlarni yaratish
    access_token = security.create_access_token(data={"sub": user.email})
    refresh_token = security.create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
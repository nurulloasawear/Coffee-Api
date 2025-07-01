from fastapi import Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.db import crud
from app.db.schemas import user as user_schema
from app.core import security
from app.db.database import SessionLocal
from app.db.models.user import User 
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(token: str = Depends(oauth2_schema),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        token_data = security.verify_token(token,credentials_exception)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db,email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ruxsat yoq"
        )
    return current_user


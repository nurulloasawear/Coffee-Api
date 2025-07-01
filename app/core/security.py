from datetime import datetime , timedelta,timezone
from typing import Optional
from jose import JWTError,jwt
from passlib.context import CryptContext
from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.db.schemas.user import TokenData

#password hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password:str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)
def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def create_access_token(data:dict,expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
def create_refresh_token(data:dict):
    expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(data=data,expires_delta=expires)
def verify_token(token:str,credentials_exception) ->TokenData:
    try:
        payload = jwt.decode(token,JWT_SECRET_KEY,algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data

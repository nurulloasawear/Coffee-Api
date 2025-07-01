from sqlalchemy import Column, Integer, String ,Boolean ,DateTime,text
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True,nullable=False)
    first_name = Column(String,nullable=True)
    last_name = Column(String,nullable=True)
    hashed_password = Column(String,nullable=False)
    is_verified = Column(Boolean,default=False)
    role = Column(String,default="simple_user")
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))


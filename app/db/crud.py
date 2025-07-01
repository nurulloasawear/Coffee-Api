from sqlalchemy.orm import Session 
from app.db.models.user import User
from app.db.schemas.user import UserCreate,UserAdminUpdate
from app.core.security import get_password_hash
def get_user_by_email(db: Session,email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,user:UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_users(db: Session,skip: int = 0,limit:int=100):
    return db.query(User).offset(skip).limit(limit).all()
def get_users_by_id(db:Session,user_id:int):
    return db.query(User).filter(User.id == user_id).first()
def update_user_by_admin(db: Session,db_user:User, user_in:UserAdminUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    print(update_data)
    for key,value in update_data.items():
        setattr(db_user,key,value)
    db.add(db_user)
    db.commit()    
    db.refresh(db_user)
    return db_user
def delete_user(db: Session, user_id:int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

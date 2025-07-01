from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.schemas import user as user_schema
from app.api.v1 import deps
from app.db.models.user import User
from app.db import crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=user_schema.UserResponse)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    return current_user


@router.get("/", response_model=List[user_schema.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    admin_user: User = Depends(deps.get_current_admin_user)
):

    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=user_schema.UserResponse)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(deps.get_db),
    admin_user: User = Depends(deps.get_current_admin_user)
):

    db_user = crud.get_users_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=user_schema.UserResponse)
def update_user_admin(
    user_id: int,
    user_in: user_schema.UserAdminUpdate,
    db: Session = Depends(deps.get_db),
    admin_user: User = Depends(deps.get_current_admin_user),
):

    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.update_users_by_admin(db=db, db_user=db_user, user_in=user_in)
    return user

@router.delete("/{user_id}", response_model=user_schema.UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    admin_user: User = Depends(deps.get_current_admin_user),
):

    db_user = crud.get_users_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return deleted_user
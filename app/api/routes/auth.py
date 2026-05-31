from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterSchema, LoginSchema, TokenSchema
from app.schemas.user import UserSchema
from app.db.session import get_db
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_token_for_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema)
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    user = register_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return user


@router.post("/login", response_model=TokenSchema)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_token_for_user(user)

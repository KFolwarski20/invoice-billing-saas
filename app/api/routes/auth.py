from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError

from app.schemas.auth import (
    RegisterSchema,
    LoginSchema,
    TokenSchema,
    RefreshSchema,
)

from app.schemas.user import UserSchema
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_token_for_user,
    verify_refresh_token,
)

from app.core.security import decode_token

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


@router.post("/refresh", response_model=TokenSchema)
def refresh(payload: RefreshSchema, db: Session = Depends(get_db)):
    user = verify_refresh_token(db, payload.refresh_token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return create_token_for_user(user)


@router.get("/me", response_model=UserSchema)
def me(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    token = authorization.replace("Bearer ", "")

    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

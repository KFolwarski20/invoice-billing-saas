from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)


def register_user(db: Session, email: str, password: str)\
        -> User | None:
    existing = db.scalar(select(User).where(User.email == email))

    if existing:
        return None

    user = User(
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str)\
        -> User | None:
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def create_token_for_user(user: User):
    return {
        "access_token": create_access_token(subject=str(user.id)),
        "refresh_token": create_refresh_token(subject=str(user.id)),
        "token_type": "bearer",
    }


def verify_refresh_token(db: Session, refresh_token: str):
    payload = decode_refresh_token(refresh_token)

    if not payload:
        return None

    user_id = payload.get("sub")

    return db.query(User).filter(User.id == user_id).first()

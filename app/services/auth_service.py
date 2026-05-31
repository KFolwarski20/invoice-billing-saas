from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
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
    return create_access_token(subject=str(user.id))

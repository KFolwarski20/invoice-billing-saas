from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserSchema(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        from_attributes = True

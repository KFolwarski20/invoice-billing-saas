from pydantic import BaseModel, EmailStr
from uuid import UUID


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    company: str | None = None


class CustomerResponse(BaseModel):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
)
from app.services import customer_service


router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    return customer_service.create_customer(
        db,
        data,
    )


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def list_customers(
    db: Session = Depends(get_db),
):
    return customer_service.get_customers(
        db,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    customer = customer_service.get_customer(
        db,
        customer_id,
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: UUID,
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    customer = customer_service.update_customer(
        db,
        customer_id,
        data,
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.delete(
    "/{customer_id}",
)
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    customer = customer_service.delete_customer(
        db,
        customer_id,
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return {
        "message": "Customer deleted"
    }

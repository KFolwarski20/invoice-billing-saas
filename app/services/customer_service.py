from uuid import UUID

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(
        db: Session,
        data: CustomerCreate,
        user_id: UUID,
):
    customer = Customer(
        **data.model_dump(),
        user_id=user_id,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers(db: Session, user_id: UUID):
    return (
        db.query(Customer)
        .filter(Customer.user_id == user_id)
        .all()
    )


def get_customer(
        db: Session,
        customer_id: UUID,
        user_id: UUID,
):
    return (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.user_id == user_id
        )
        .first()
    )


def update_customer(
        db: Session,
        customer_id: UUID,
        user_id: UUID,
        data: CustomerCreate,
):
    customer = get_customer(
        db,
        customer_id,
        user_id
    )

    if not customer:
        return None

    for key, value in data.model_dump().items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(
        db: Session,
        customer_id: UUID,
        user_id: UUID,
):
    customer = get_customer(
        db,
        customer_id,
        user_id,
    )

    if not customer:
        return None

    db.delete(customer)
    db.commit()

    return customer

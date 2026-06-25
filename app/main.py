from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.customers import router as customer_router

app = FastAPI(title="Invoice Billing SaaS")

app.include_router(auth_router)
app.include_router(customer_router)


@app.get("/")
def root():
    return {"status": "OK"}

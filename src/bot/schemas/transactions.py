from pydantic import BaseModel


class CreateTransactionSchema(BaseModel):
    amount: int
    customer_id: int
    requisite_id: int


class AddCheckTransactionSchema(BaseModel):
    transaction_id: int
    check_path: str

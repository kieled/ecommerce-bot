from pydantic import BaseModel


class CreateCustomerSchema(BaseModel):
    telegram_chat_id: str
    instagram: str | None = None
    username: str | None = None


class CreateAddressSchema(BaseModel):
    address: str
    city: str
    postal_index: int
    first_name: str
    last_name: str
    country: str
    customer_id: int

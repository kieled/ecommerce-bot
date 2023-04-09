from pydantic import BaseModel


class CreateOrderSchema(BaseModel):
    product_id: int
    product_color_id: int
    product_size_id: int | None = None
    customer_address_id: int
    transaction_id: int

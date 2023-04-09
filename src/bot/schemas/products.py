from pydantic import BaseModel


class ColorSchema(BaseModel):
    id: int
    name: str

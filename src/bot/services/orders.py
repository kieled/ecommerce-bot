from sqlalchemy import insert

from db import Order
from bot import schemas
from .helper import AppService


class OrderService(AppService):
    async def create(self, payload: schemas.CreateOrderSchema) -> int:
        sql = insert(Order).values(**payload.dict()).returning(Order.id)
        order_id: int = (await self.db.execute(sql)).scalars().first()
        await self.db.commit()
        return order_id

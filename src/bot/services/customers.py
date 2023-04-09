from sqlalchemy import select, insert
from sqlalchemy.orm import load_only, joinedload

from db import CustomerAddress, User
from bot.schemas import CreateCustomerSchema, CreateAddressSchema
from .helper import AppService


class CustomerService(AppService):
    async def create(self, payload: CreateCustomerSchema) -> int | None:
        sql = insert(User).values(
            **payload.dict(exclude_none=True)
        ).returning(User.id)
        customer_id = (await self.db.execute(sql)).scalars().first()
        await self.db.commit()
        return customer_id

    async def get_addresses(self, customer_tg: int | str) -> list[CustomerAddress]:
        sql = select(User).options(
            load_only(User.id),
            joinedload(User.addresses)
        ).where(User.telegram == str(customer_tg))
        data = (await self.db.execute(sql)).scalars().first()
        if not data:
            return []
        return data.addresses

    async def add_address(self, payload: CreateAddressSchema) -> int | None:
        sql = insert(CustomerAddress).values(
            **payload.dict()
        ).returning(CustomerAddress.id)
        customer_address_id = (await self.db.execute(sql)).scalars().first()
        await self.db.commit()
        return customer_address_id

    async def get_customer(self, tg_chat_id: int) -> User | None:
        sql = select(User).where(User.telegram == str(tg_chat_id))
        customer_id = (await self.db.execute(sql)).scalars().first()
        return customer_id

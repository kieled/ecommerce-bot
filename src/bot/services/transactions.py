from db import Transaction
from sqlalchemy import insert, update

from bot import schemas

from .helper import AppService


class TransactionService(AppService):
    async def create(self, payload: schemas.CreateTransactionSchema) -> int:
        sql = insert(Transaction).values(**payload.dict()).returning(Transaction.id)
        transaction_id: int = (await self.db.execute(sql)).scalars().first()
        await self.db.commit()
        return transaction_id

    async def add_check(self, payload: schemas.AddCheckTransactionSchema) -> None:
        sql = (
            update(Transaction)
            .where(Transaction.id == payload.transaction_id)
            .values(check_path=payload.check_path)
        )
        await self.db.execute(sql)
        await self.db.commit()

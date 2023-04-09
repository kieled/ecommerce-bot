from sqlalchemy import select
from db import Requisites
from .helper import AppService


class RequisiteService(AppService):
    async def get_active(self) -> Requisites:
        sql = select(Requisites).where(Requisites.is_active == True)
        result = (await self.db.execute(sql)).scalars().first()
        return result

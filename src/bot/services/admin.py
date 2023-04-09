from sqlalchemy import select
from db import User
from .helper import AppService


class AdminService(AppService):
    async def get_tg(self) -> list[str]:
        sql = select(User.telegram_chat_id).where(User.telegram_chat_id != None)
        return (await self.db.execute(sql)).scalars().unique().all()

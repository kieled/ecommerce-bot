from datetime import datetime, timedelta

from aiohttp import ClientSession
from db import models, session
from sqlalchemy import insert, select, update


def find_rates(json: dict) -> dict:
    result = {}
    for i in json['rates']:
        if i['buyIso'] == 'BYN':
            if i['sellIso'] == 'RUB':
                result['rub'] = i['buyRate']
            if i['sellIso'] == 'USD':
                result['usd'] = i['buyRate']
    return result


class PricesManager:
    def __init__(self):
        self._url: str = 'https://developerhub.alfabank.by:8273/partner/1.0.1/public/rates'
        self._usd: float = 0.0
        self._rub: float = 0.0
        self._last_update: datetime | None = None

    async def get(self):
        if self._last_update < (datetime.now() - timedelta(days=1)):
            await self._update()
            await self._save()
        return {'usd': self._usd, 'rub': self._rub}

    async def _update(self):
        async with ClientSession() as s:
            async with s.get(self._url) as response:
                result = find_rates(await response.json())
                self._usd = result['usd']
                self._rub = result['rub']

    async def _save(self):
        async with session() as s:
            sql = update(models.Settings).values(usd=self._usd, rub=self._rub)
            self._last_update = datetime.now()
            await s.execute(sql)
            await s.commit()

    async def load(self):
        async with session() as s:
            sql = select(models.Settings).limit(1)
            data: models.Settings = (await s.execute(sql)).scalars().first()
            if not data:
                await self._update()
                await s.execute(insert(models.Settings).values(usd=self._usd, rub=self._rub))
                return await s.commit()
            if (data.updated_at < (datetime.now() - timedelta(days=1))) or not data.updated_at:
                await self._update()
                await self._save()
            self._last_update = data.updated_at
            self._rub = data.rub
            self._usd = data.usd


prices_manager = PricesManager()

__all__ = ['prices_manager']

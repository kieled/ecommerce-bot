from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy.sql import Select
from db import Product, ProductStock, ProductSize


class ProductService:
    def __init__(self, db: AsyncSession, product_id: int | None = None):
        self._db = db
        self._product_id = product_id

    async def fetch_one(self, sql: Select):
        if not self._product_id:
            raise Exception('Product id should be set for call this method')
        return (await self._db.execute(sql.where(Product.id == self._product_id))).scalars().first()

    async def get_product_by_id(self) -> Product | None:
        sql = select(Product).options(load_only(Product.id, Product.title, Product.price))
        return await self.fetch_one(sql)

    async def get_product_colors(self) -> Product | None:
        sql = select(Product).options(
            load_only(Product.id),
            joinedload(Product.stocks).load_only(
                ProductStock.color, ProductStock.name, ProductStock.id
            ),
        )
        return await self.fetch_one(sql)

    async def get_product_sizes(self, product_stock_id: int) -> ProductStock | None:
        sql = (
            select(ProductStock)
            .options(
                load_only(ProductStock.id),
                joinedload(ProductStock.sizes).load_only(
                    ProductSize.size, ProductSize.name, ProductSize.id
                ),
            )
            .where(ProductStock.id == product_stock_id)
        )
        return (await self._db.execute(sql)).scalars().first()

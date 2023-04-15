from db.models import (
    CustomerAddress,
    Order,
    Product,
    ProductCategory,
    ProductParam,
    ProductSize,
    ProductStock,
    Promo,
    Requisites,
    RequisiteTypes,
    Settings,
    Transaction,
    User,
)
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_exclude_list = [User.password]


class ProductSizeAdmin(ModelView, model=ProductSize):
    pass


class OrderAdmin(ModelView, model=Order):
    pass


class PromoAdmin(ModelView, model=Promo):
    pass


class ProductAdmin(ModelView, model=Product):
    column_exclude_list = [Product.images, Product.updated_at]


class ProductParamAdmin(ModelView, model=ProductParam):
    pass


class ProductStockAdmin(ModelView, model=ProductStock):
    column_exclude_list = [ProductStock.image]


class ProductCategoryAdmin(ModelView, model=ProductCategory):
    pass


class CustomerAddressAdmin(ModelView, model=CustomerAddress):
    pass


class RequisiteTypesAdmin(ModelView, model=RequisiteTypes):
    pass


class RequisitesAdmin(ModelView, model=Requisites):
    pass


class SettingsAdmin(ModelView, model=Settings):
    pass


class TransactionAdmin(ModelView, model=Transaction):
    pass


__all__ = [
    'UserAdmin',
    'ProductSizeAdmin',
    'OrderAdmin',
    'PromoAdmin',
    'ProductAdmin',
    'ProductParamAdmin',
    'ProductStockAdmin',
    'ProductCategoryAdmin',
    'CustomerAddressAdmin',
    'RequisiteTypesAdmin',
    'RequisitesAdmin',
    'SettingsAdmin',
    'TransactionAdmin',
]

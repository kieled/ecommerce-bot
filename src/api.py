from contextlib import asynccontextmanager

from admin import views as admin_views
from db import config
from fastapi import FastAPI
from parsers import prices_manager
from sqladmin import Admin


@asynccontextmanager
async def lifespan(_: FastAPI):
    await prices_manager.load()
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, config.engine)

for i in admin_views.__all__:
    if 'Admin' in i:
        admin.add_view(getattr(admin_views, i))


@app.get('/status')
async def status_check():
    return {'status': 'ok'}

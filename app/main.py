from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from sqladmin import Admin, ModelView

from app.bookings.router import router as router_bookings
from app.database import engine
from app.users.models import Users
from app.users.router import router as router_auth
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images

from app.config import settings

app = FastAPI(title='Bookit!')
admin = Admin(app, engine)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_auth)

app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


class UserAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]


admin.add_view(UserAdmin)

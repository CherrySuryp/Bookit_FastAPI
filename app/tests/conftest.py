import asyncio
import json
from datetime import datetime
from functools import wraps

from httpx import AsyncClient

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from unittest import mock


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


# Disables fastapi-cache during testing
def mock_cache(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)
        return inner
    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()


@pytest.fixture(scope="module")
async def ac():
    from app.main import app as fastapi_app # Disables fastapi-cache during testing
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    from app.main import app as fastapi_app # Disables fastapi-cache during testing
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        await ac.post('/auth/login', json={
            "email": "test@test.com",
            "password": "test"
        })
        assert ac.cookies["booking_access_token"]
        yield ac


@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

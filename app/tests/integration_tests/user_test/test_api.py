import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("pes@kot.com", "peskot", 200),
        ("kot@pes.com", "kot0pes", 409),
        ("abcde", "kotopes", 422),
    ],
)
async def test_register_user(ac: AsyncClient, email, password, status_code):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("artem@example.com", "art3m", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "test", 200),
    ],
)
async def test_login_user(email, password, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/auth/me")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("testt@test.com", "test", 200),
        ("artemm@example.com", "artem", 200),
        ("iparkhipychev@gmail.com", "mark", 200),
    ],
)
async def test_reg_login_logout(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code

    get_cookie = ac.cookies.values()
    assert get_cookie is not None

    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code

    response = await ac.get("/auth/me")
    assert response.status_code == status_code

    response = await ac.post("/auth/logout")
    assert response.status_code == status_code

    response = await ac.get("/auth/me")
    assert response.status_code == 401

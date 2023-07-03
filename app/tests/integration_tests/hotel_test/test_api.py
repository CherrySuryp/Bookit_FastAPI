import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        ("Алтай", "2023-01-01", "2023-01-10", 200),
        ("Коми", "2023-01-01", "2023-01-10", 200),
        ("ГНПА", "2023-01-01", "2023-01-10", 404),
        ("Алтай", "2023-01-01", "2023-02-10", 403),
        ("Коми", "2023-02-01", "2023-01-01", 400),
    ],
)
async def test_find_hotel_by_location_and_dates(
    location, date_from, date_to, status_code, ac: AsyncClient
):
    response = await ac.get(
        f"/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "hotel_id, status_code",
    [
        (1, 200),
        (2, 200),
        (3, 200),
        (4, 200),
        (5, 200),
        (6, 200),
        (7, 404),
        (8, 404),
        (9, 404),
    ],
)
async def test_get_hotel_by_id(hotel_id, status_code, ac: AsyncClient):
    response = await ac.get(f"/hotels/id/{hotel_id}")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "hotel_id, date_from, date_to, status_code",
    [
        (1, "2023-01-01", "2023-01-30", 200),
        (2, "2023-01-01", "2023-01-30", 200),
        (3, "2023-01-01", "2023-01-30", 200),
        (4, "2023-01-01", "2023-01-30", 200),
        (5, "2023-01-01", "2023-01-30", 200),
        (6, "2023-01-30", "2023-01-01", 400),
        (3, "2023-01-30", "2023-01-01", 400),
        (0, "2023-01-30", "2023-02-01", 404),
        (-1, "2023-01-30", "2023-02-01", 404),
        (1, "2023-01-30", "2023-02-30", 422),
        (1, "2023-01-30", "2023-03-30", 403),
    ],
)
async def test_get_rooms_by_hotel_id_and_dates(
    hotel_id, date_from, date_to, status_code, ac: AsyncClient
):
    response = await ac.get(
        f"/hotels/{hotel_id}/rooms", params={"date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code

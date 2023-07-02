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

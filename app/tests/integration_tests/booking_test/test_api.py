import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, email_to, status_code", [
    *[(4, "2030-05-01", "2030-05-15", "iparkhipychev@gmail.com", 200)] * 8,
    (4, "2030-05-01", "2030-05-15", "iparkhipychev@gmail.com", 409),
    (4, "2030-05-01", "2030-05-15", "iparkhipychev@gmail.com", 409),
])
async def test_add_and_get_booking(
        room_id, date_from, date_to, email_to,
        status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
        "email_to": email_to
    })

    assert response.status_code == status_code


async def test_add_and_delete_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    assert response

    for i in response.json():
        await authenticated_ac.delete("/bookings", params={"booking_id": i['id']})

    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 409

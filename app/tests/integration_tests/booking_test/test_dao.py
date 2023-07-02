import sys

sys.dont_write_bytecode = True
from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    find_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert find_booking is not None


async def test_add_get_and_delete_booking():
    user_id = 1
    room_id = 2
    date_from = "2023-07-24"
    date_to = "2023-07-24"

    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime(date_from, "%Y-%m-%d"),
        date_to=datetime.strptime(date_to, "%Y-%m-%d"),
    )
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    find_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert find_booking is not None

    await BookingDAO.delete(user_id=new_booking.user_id, booking_id=new_booking.id)
    result = await BookingDAO.find_one_or_none(id=new_booking.id)

    assert result is None

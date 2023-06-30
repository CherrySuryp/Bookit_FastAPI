from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCanNotBeBooked, BookingDoesntExistException, BookingsDoesNotExistException

from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.find_all(user_id=user.id)
    if not result:
        raise BookingsDoesNotExistException
    return result


@router.post('')
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked


@router.delete('')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    existing_booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if not existing_booking:
        raise BookingDoesntExistException
    await BookingDAO.delete(user.id, booking_id)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

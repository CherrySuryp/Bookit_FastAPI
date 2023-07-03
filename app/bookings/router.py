from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_versioning import version
from pydantic import EmailStr

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import (
    BookingDoesntExistException,
    BookingsDoesNotExistException,
    RoomCanNotBeBooked, TooMuchDaysException, WrongDateEntryException,
)
from app.tasks.task import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.find_all(user_id=user.id)
    if not result:
        raise BookingsDoesNotExistException
    return result


@router.post("")
@version(1)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    if (date_to - date_from).days > 30:
        raise TooMuchDaysException  # 403
    if date_to < date_from:
        raise WrongDateEntryException  # 400
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked # 409
    send_booking_confirmation_email.delay(email_to=user.email)


@router.delete("")
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    existing_booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if not existing_booking:
        raise BookingDoesntExistException
    await BookingDAO.delete(user.id, booking_id)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

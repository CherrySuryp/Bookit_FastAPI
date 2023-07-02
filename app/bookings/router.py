from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import (
    BookingDoesntExistException,
    BookingsDoesNotExistException,
    RoomCanNotBeBooked,
)
from app.tasks.task import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.find_all(user_id=user.id)
    if not result:
        raise BookingsDoesNotExistException
    return result


@router.post("")  # Don't forget to return param email_to: EmailStr,
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    email_to: EmailStr,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked
    send_booking_confirmation_email.delay(email_to=email_to)


@router.delete("")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    existing_booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if not existing_booking:
        raise BookingDoesntExistException
    await BookingDAO.delete(user.id, booking_id)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

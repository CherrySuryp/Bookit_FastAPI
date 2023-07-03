from datetime import date

from fastapi import APIRouter

from app.exceptions import RoomsOrHotelNotFoundException, TooMuchDaysException, WrongDateEntryException
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel_and_date(
    hotel_id: int, date_from: date, date_to: date
) -> list[SRooms]:
    if (date_to - date_from).days > 30:
        raise TooMuchDaysException  # 403
    if date_to < date_from:
        raise WrongDateEntryException  # 400
    result = await RoomsDAO.get_available_rooms_by_hotel_and_dates(
        hotel_id, date_from, date_to
    )
    if not result:
        raise RoomsOrHotelNotFoundException
    return result

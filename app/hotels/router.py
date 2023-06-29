from datetime import date

from fastapi import APIRouter

from app.exceptions import HotelNotFoundException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)


@router.get('/{location}')
async def get_hotels(location: str, date_from: date, date_to: date):
    pass


@router.get('/id/{hotel_id}')
async def get_a_specific_hotel(hotel_id: int) -> SHotel:
    result = await HotelsDAO.find_one_or_none(id=hotel_id)
    if not result:
        raise HotelNotFoundException
    return result

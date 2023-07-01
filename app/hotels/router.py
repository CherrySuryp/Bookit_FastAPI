import asyncio
from datetime import date
from unittest import mock

from fastapi import APIRouter

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()  # Disables cache for pytest
from fastapi_cache.decorator import cache

from app.exceptions import HotelNotFoundException, AvailableHotelsNotFoundException, TooMuchDaysException, \
    WrongDateEntryException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SFindHotel

router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)


@router.get('/{location}')
@cache(expire=60)
async def get_hotels_by_location_and_time(location: str, date_from: date, date_to: date):
    await asyncio.sleep(2)
    if (date_to - date_from).days > 30:
        raise TooMuchDaysException  # 403
    if date_to < date_from:
        raise WrongDateEntryException  # 400
    found_hotels = await HotelsDAO.find_hotels_by_location_and_date(location, date_from, date_to)
    if not found_hotels:
        raise AvailableHotelsNotFoundException  # 404
    return found_hotels


@router.get('/id/{hotel_id}')
async def get_a_specific_hotel(hotel_id: int) -> SHotel:
    result = await HotelsDAO.find_one_or_none(id=hotel_id)
    if not result:
        raise HotelNotFoundException
    return result

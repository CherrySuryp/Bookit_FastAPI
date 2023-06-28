from datetime import date

from fastapi import APIRouter

router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)


@router.get('/{location}')
def get_hotels(location: str, date_from: date, date_to: date):
    pass


@router.get('/id/{hotel_id}')
def get_a_specific_hotel(hotel_id: int):
    pass

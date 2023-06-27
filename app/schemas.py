from pydantic import BaseModel
from datetime import date


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SHotel(BaseModel):
    location: str
    date_from: date
    date_to: date
    has_spa: bool
    stars: int

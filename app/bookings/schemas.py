from datetime import date

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int = 1
    room_id: int = 12
    user_id: int = 1
    date_from: date
    date_to: date
    price: int = 9900
    total_days: int = 2
    total_cost: int = 19800
    image_id: int
    name: str
    description: str
    services: list

    class Config:
        orm_mode = True

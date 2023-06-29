import typing

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int = 100
    name: str = "Bear's house"
    location: str = 'Russia, Altay Republic'
    service: list = [
        "Wi-Fi",
        "Pool",
        "Parking",
        "Conditioner"
    ]
    rooms_quantity: int = 5
    image_id: int = 23545

    class Config:
        orm_mode = True

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


class SFindHotel(BaseModel):
    id: int
    name: str
    location: str
    service: list = [
      "Wi-Fi",
      "Парковка"
    ]
    image_id: int
    rooms_quantity: int
    rooms_left: int

    class Config:
        orm_mode = True

from pydantic import BaseModel


class SRooms(BaseModel):
    room_id: int = 9
    hotel_id: int = 1
    name: str = "Bear's house"
    description: str = "Шикарный номер с видом на озеро"
    services: list = ["Бесплатный Wi‑Fi", "Кондиционер"]
    price: int = 2900
    image_id: int = 5
    total_cost: int = 9900
    rooms_quantity: int = 10
    rooms_left: int = 2

    class Config:
        orm_mode = True

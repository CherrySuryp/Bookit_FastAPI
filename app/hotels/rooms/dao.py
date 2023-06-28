from app.hotels.rooms.models import Rooms
from dao.base import BaseDAO


class RoomsDAO(BaseDAO):
    model = Rooms

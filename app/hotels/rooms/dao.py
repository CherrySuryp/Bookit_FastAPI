from datetime import date

from sqlalchemy import select, and_, or_, func

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from dao.base import BaseDAO


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_hotel_by_location(cls):
        """


        """
        pass

from datetime import date

from sqlalchemy import select, and_, or_, func

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from dao.base import BaseDAO


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_hotel(cls):
        """
        WITH available_hotels AS (
            SELECT hotels.id as hotel_id, (hotels.rooms_quantity - count(hotel_id)) AS rooms_left
            FROM hotels
            JOIN rooms on hotels.id = rooms.hotel_id
            JOIN bookings on rooms.id = bookings.room_id
            WHERE location like '%Алтай%' AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY hotels.id)

        SELECT hotels.id, hotels.name, hotels.location,
               hotels.service, hotels.image_id, hotels.rooms_quantity, coalesce(available_hotels.rooms_left,
               rooms_quantity) AS rooms_left
        FROM hotels
        FULL JOIN available_hotels ON available_hotels.hotel_id = hotels.id
        WHERE coalesce(available_hotels.rooms_left, rooms_quantity) > 0
        GROUP BY hotels.id, hotels.name, hotels.location, hotels.image_id, hotels.rooms_quantity, rooms_left
        ORDER BY rooms_left DESC
        """
        pass

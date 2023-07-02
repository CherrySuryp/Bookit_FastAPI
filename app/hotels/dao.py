from datetime import date

from sqlalchemy import and_, desc, func, or_, select

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from dao.base import BaseDAO


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_hotels_by_location_and_date(
        cls, location: str, date_from: date, date_to: date
    ):
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
        async with async_session_maker() as session:
            subquery = (
                select(
                    Hotels.id.label("hotel_id"),
                    (Hotels.rooms_quantity - func.count(Rooms.hotel_id)).label(
                        "rooms_left"
                    ),
                )
                .join(Rooms, Hotels.id == Rooms.hotel_id)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    )
                )
                .group_by(Hotels.id)
                .cte("subquery")
            )

            query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.service,
                    Hotels.image_id,
                    Hotels.rooms_quantity,
                    func.coalesce(subquery.c.rooms_left, Hotels.rooms_quantity).label(
                        "rooms_left"
                    ),
                )
                .select_from(Hotels)
                .join(subquery, subquery.c.hotel_id == Hotels.id, full=True)
                .where(
                    and_(
                        Hotels.location.like(f"%{location.capitalize()}%"),
                        func.coalesce(subquery.c.rooms_left, Hotels.rooms_quantity) > 0,
                    )
                )
                .order_by(desc("rooms_left"))
            )

            result = await session.execute(query)
            return result.mappings().all()

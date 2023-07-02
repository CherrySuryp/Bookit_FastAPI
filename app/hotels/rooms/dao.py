from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from dao.base import BaseDAO


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_available_rooms_by_hotel_and_dates(
        cls, hotel_id: int, date_from: date, date_to: date
    ):
        """
        WITH subquery AS (
        SELECT room_id, (rooms.quantity - count(room_id)) as rooms_left
        FROM bookings
        JOIN rooms on rooms.id = bookings.room_id
        JOIN hotels on rooms.hotel_id = hotels.id
        WHERE hotels.id = 5 AND
        (
        (bookings.date_from >= '2024-01-02' AND bookings.date_from <= '2024-01-10') OR
        (bookings.date_from <= '2024-01-02' AND bookings.date_to > '2024-01-02')
        )
        GROUP BY room_id, rooms.quantity
        )

        SELECT rooms.id, rooms.hotel_id, rooms.name, rooms.description,
        rooms.services, rooms.price, rooms.image_id, rooms.quantity,
        coalesce(subquery.rooms_left, rooms.quantity) AS available_rooms,
        (10 * rooms.price) AS total_cost
        FROM rooms
        FULL JOIN subquery on subquery.room_id = rooms.id

        Ответ пользователю: для каждого
        номера должно быть указано: id, hotel_id, name, description, services, price, quantity, image_id, total_cost
        (стоимость бронирования номера за весь период),
        rooms_left (количество оставшихся номеров).
        """
        async with async_session_maker() as session:
            subquery = (
                select(
                    Bookings.room_id,
                    (
                        Rooms.quantity
                        - func.count(Bookings.room_id).label("rooms_left")
                    ).label("rooms_left"),
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id)
                .join(Hotels, Rooms.hotel_id == Hotels.id)
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
                .group_by(Bookings.room_id, Rooms.quantity)
                .cte("subquery")
            )

            stmt = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                    Rooms.price,
                    Rooms.image_id,
                    Rooms.quantity,
                    func.coalesce(subquery.c.rooms_left, Rooms.quantity).label(
                        "available_rooms"
                    ),
                    ((date_to - date_from).days * Rooms.price).label("total_cost"),
                )
                .select_from(Rooms)
                .join(subquery, subquery.c.room_id == Rooms.id, full=True)
                .filter(Rooms.hotel_id == hotel_id)
            )

            result = await session.execute(stmt)
            return result.mappings().all()

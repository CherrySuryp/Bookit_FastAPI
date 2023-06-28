from fastapi import FastAPI, Query, Depends
from datetime import date
from typing import Optional

from app.bookings.router import router as router_bookings
from app.users.router import router as router_auth
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

app = FastAPI(title='Booking')
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)


# class HotelSearchArgs:
#     def __init__(
#             self,
#             location: str,
#             date_from: date,
#             date_to: date,
#             has_spa: Optional[bool] = None,
#             stars: Optional[int] = Query(None, ge=1, le=5)
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars
#
#
# @app.get("/hotels", response_model=list[SHotel])
# def get_hotels(search_args: HotelSearchArgs = Depends()):
#     return search_args

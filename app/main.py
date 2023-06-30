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


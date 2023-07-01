from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]


class BookingsAdmin(ModelView, model=Bookings):
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-book"
    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True
    column_list = [c.name for c in Bookings.__table__.c]


class RoomsAdmin(ModelView, model=Rooms):
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [c.name for c in Rooms.__table__.c]


class HotelsAdmin(ModelView, model=Hotels):
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [c.name for c in Hotels.__table__.c]


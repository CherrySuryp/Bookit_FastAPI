from app.hotels.models import Hotels
from dao.base import BaseDAO


class HotelsDAO(BaseDAO):
    model = Hotels

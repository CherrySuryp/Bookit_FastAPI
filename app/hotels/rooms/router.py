from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)


@router.get('/{hotel_id}/rooms')
def get_all_rooms(hotel_id, user: Users = Depends(get_current_user)):
    pass

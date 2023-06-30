from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.exceptions import UserAlreadyExistsException
from app.users.auth import get_password, verify_password, auth_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schema import SUserReg

router = APIRouter(
    prefix='/auth',
    tags=['Reg and auth']
)


@router.post('/reg')
async def reg_user(user_data: SUserReg):
    existing_user = await UsersDAO.find_one_or_none(
        email=user_data.email
    )
    # Before registration, we check if user exists
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login(response: Response, user_data: SUserReg):
    user = await auth_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie("booking_access_token")
    return status.HTTP_200_OK


@router.get('/me')
async def read_user_me(user: Users = Depends(get_current_user)):
    return user

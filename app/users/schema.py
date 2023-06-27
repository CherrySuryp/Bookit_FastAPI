from pydantic import BaseModel, EmailStr


class SUserReg(BaseModel):
    email: EmailStr
    password: str

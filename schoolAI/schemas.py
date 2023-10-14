from pydantic import BaseModel, EmailStr, constr, validator
from typing import List


class RegisterSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=5, max_length=20)
    confirm_password: str

    @validator("confirm_password")
    def passwords_are_same(cls, confirm_password, values):
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password


class LoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=5, max_length=20)


class TopicSchema(BaseModel):
    topics: List[constr(min_length=5)]

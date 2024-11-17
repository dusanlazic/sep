from pydantic import BaseModel


class UserRegistrationRequest(BaseModel):
    username: str
    password: str
    full_name: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserBriefDataResponse(BaseModel):
    username: str
    full_name: str

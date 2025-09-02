from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str


class Session(BaseModel):
    user_id: int
    session_id: str

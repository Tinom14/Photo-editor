from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from http_service.src.schemas.exceptions import LoginAlreadyExistsError, NotFoundError, InvalidCredentialsError
from http_service.src.schemas.schemas import AuthRequest
from http_service.src.usecases.abstract_user_service import AbstractUserService
from http_service.src.usecases.abstract_session_service import AbstractSessionService
from http_service.src.dependencies.user_depend import get_user_service
from http_service.src.dependencies.session_depend import get_session_service


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: AuthRequest, service: Annotated[AbstractUserService, Depends(get_user_service)]):
    try:
        user_id = await service.create_user(user.username, user.password)
        return user_id
    except LoginAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This login is already taken"
        )


@router.post("/login")
async def login_user(user: AuthRequest, user_service: Annotated[AbstractUserService, Depends(get_user_service)],
                     session_service: Annotated[AbstractSessionService, Depends(get_session_service)]):
    try:
        user_id = await user_service.login_user(user.username, user.password)
        token = await session_service.create_session(user_id)
        return {"token": token}
    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Login not found",
            headers={"Error": "Login not found"}
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid password",
            headers={"Error": "Invalid password"}
        )

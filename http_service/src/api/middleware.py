from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from typing import Annotated
from http_service.src.usecases.abstract_session_service import AbstractSessionService
from http_service.src.dependencies.session_depend import get_session_service

security_scheme = HTTPBearer(auto_error=False)


async def get_current_session(
        session_service: Annotated[AbstractSessionService, Depends(get_session_service)],
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session_id = credentials.credentials
    session = await session_service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return session
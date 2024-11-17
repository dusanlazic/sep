from uuid import UUID

import jwt
from fastapi import HTTPException, Request

from ..config import config


def get_current_user(request: Request) -> UUID:
    """
    Returns the current user's ID.

    :return: Current user's ID.
    :rtype: UUID
    """
    token: str | None = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token not provided.")

    try:
        decoded = jwt.decode(token, config.jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid access token.")
    
    user_id = decoded.get("id")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in access token.")
    
    return UUID(user_id)

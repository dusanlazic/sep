from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Cookie, Header, HTTPException

from ..config import config


def get_current_merchant_manager_id(
    access_token: Annotated[str | None, Cookie()] = None,
) -> UUID:
    """
    Returns the current user's ID. This authenticates the user that manages the shop.

    :return: Current user's ID.
    :rtype: UUID
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not provided.")

    data = jwt.decode(
        access_token,
        config.secret_key.get_secret_value(),
        algorithms=["HS256"],
    )
    return UUID(data["sub"])


def get_current_merchant(
    api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> UUID:
    """
    Returns the current merchant's ID. This authenticates the request coming from the
    web shop application.

    :return: Current merchant's ID.
    :rtype: UUID
    """
    if not api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header not set.")

    # TODO: API key validation, merchant lookup and retrieval.
    # Consider switching to returning the actual merchant object.
    return UUID("00000000-0000-0000-0000-000000000000")


def is_admin(
    access_token: Annotated[str | None, Cookie()] = None,
) -> bool:
    """
    Returns whether the request is coming from an admin user.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not provided.")

    return access_token == config.admin_secret.get_secret_value()

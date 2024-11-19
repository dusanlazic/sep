from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Header, HTTPException


def get_current_merchant_manager(
    access_token: Annotated[str | None, Cookie()] = None,
) -> UUID:
    """
    Returns the current user's ID. This authenticates the user that manages the shop.

    :return: Current user's ID.
    :rtype: UUID
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not provided.")

    # TODO: Token validation and data extraction
    return UUID("00000000-0000-0000-0000-000000000000")


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

    # TODO: Token validation and data extraction
    return access_token == "admin"

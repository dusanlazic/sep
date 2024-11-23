from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Cookie, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..config import config
from ..database import get_db
from ..merchants import service as merchant_service
from ..merchants.models import Merchant


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
    db: Session = Depends(get_db),
) -> Merchant:
    """
    Returns the current merchant's ID. This authenticates the request coming from the
    web shop application.

    :return: Current merchant's ID.
    :rtype: UUID
    """
    if not api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header not set.")

    merchant = merchant_service.get_merchant_by_api_key(db, api_key)
    if not merchant:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    return merchant


def is_admin(
    access_token: Annotated[str | None, Cookie()] = None,
) -> bool:
    """
    Returns whether the request is coming from an admin user.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not provided.")

    return access_token == config.admin_secret.get_secret_value()

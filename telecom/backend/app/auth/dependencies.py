from uuid import UUID

from fastapi import HTTPException, Request
from pydantic import SecretStr


def get_current_user(request: Request) -> UUID:
    """
    Returns the current user's ID.

    :return: Current user's ID.
    :rtype: UUID
    """
    token: SecretStr | None = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token not provided.")

    # TODO: Token validation and data extraction
    return UUID("00000000-0000-0000-0000-000000000000")

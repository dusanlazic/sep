from fastapi import APIRouter

from .schemas import BarResponse, FooRequest

router = APIRouter(prefix="/hello", tags=["Hello World"])


@router.post("/foo", response_model=BarResponse)
def foo(request: FooRequest):
    return BarResponse(buzz=len(request.fizz))


# There may be more than one router to separate different parts of the API.
# router = APIRouter(prefix="/users", tags=["User Management"])


# @router.post("/foo", response_model=BarResponse)
# def foo(request: FooRequest):
#     return BarResponse(buzz=len(request.fizz))

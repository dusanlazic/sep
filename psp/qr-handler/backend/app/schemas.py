from pydantic import BaseModel


class FooRequest(BaseModel):
    fizz: str


class BarResponse(BaseModel):
    buzz: int

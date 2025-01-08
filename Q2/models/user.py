from pydantic import BaseModel

class User(BaseModel):
    name: str
    height: float
    weight: float
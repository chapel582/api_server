from pydantic import BaseModel


class Student(BaseModel):
    name: str
    id: int
    score: int

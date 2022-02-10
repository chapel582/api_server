from pydantic import BaseModel


# TODO: delete this test code
class Student(BaseModel):
    name: str
    id: int
    score: int


class Org(BaseModel):
    id: int
    org_name: str

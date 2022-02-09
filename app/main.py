from typing import Dict, Set

from fastapi import FastAPI

from models import Student

app = FastAPI()


@app.get("/")
def hello() -> str:
    """
    A hello world endpoint
    """
    return "Hello World!"


@app.get("/info")
def info(limit: int = 1, score: int = 90) -> Dict[str, str]:
    if score > 90:
        return {"info": f"{limit} records with a score above 90 from the database"}
    else:
        return {"info": f"{limit} records from the database"}


@app.post("/info")
def create(request: Student) -> Dict[str, str]:
    return {"record": f"New record is created with {request.name}"}


@app.get("/info/{name}")
def display(name: str) -> Dict[str, str]:
    return {"info": name}


@app.get("/info/{user_id}/score")
def score(user_id: int) -> Dict[int, Set[str]]:
    return {user_id: {"87", "91"}}

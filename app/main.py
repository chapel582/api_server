from typing import Dict, Set

from fastapi import FastAPI
from dotenv import load_dotenv

from illu_db import init_db
from illu_models import Student

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:  # pragma no cover
    """
    Setup Postgres DB connection
    """
    load_dotenv()
    init_db()


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

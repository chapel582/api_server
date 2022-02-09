from fastapi import FastAPI

from typing import Dict, Set

app = FastAPI()


@app.get("/")
def hello() -> str:
    """
    A hello world endpoint
    """
    return "Hello World!"


@app.get("/info")
def info() -> Dict[str, Set[str]]:
    return {"info": {"information page"}}


@app.get("/info/{name}")
def display(name: str) -> Dict[str, str]:
    return {"info": name}


@app.get("/info/{user_id}/score")
def score(user_id: int) -> Dict[int, Set[str]]:
    return {user_id: {"87", "91"}}

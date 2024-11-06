from enum import Enum
from uuid import uuid4
from typing import Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

database = []

class Sex(str, Enum):
    Male = "male"
    Female = "female"

class Human(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)

    height: float
    weight: float

    age: int

    sex: Sex

    lastName: str
    firstName: str
    middleName: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        kwargs.pop("id", None)

        super().__init__(**kwargs)

def makeErrorDict(detail: str, http_statusCode: int = 0) -> dict:
    return {"error": {"http": {"statusCode": 404}, "detail": detail}}

def makeItemDict(item: Any) -> dict:
    return {"item": item}

def makeItemsDict(items: list) -> dict:
    return {"items": items}

def addHuman(human: Human) -> Human:
    global database

    database.append(human)

    return human

def getHumanIndex(id: str) -> Optional[int]:
    for i in range(len(database)):
        if database[i].id == id:
            return i

    return None

def getHuman(id: str) -> Optional[Human]:
    humanIndex = getHumanIndex(id)

    return None if humanIndex is None else database[humanIndex]

def updateHuman(id: str, **newFields) -> dict:
    humanIndex = getHumanIndex(id)

    if humanIndex is None:
        return makeErrorDict("Human not found", 404)

    global database

    human = database[humanIndex]
    humanFields = human.__fields__

    changedFields = [field for field in humanFields if field in newFields and getattr(human, field) != newFields[field]] if len(newFields) > 0 else []

    if "sex" in changedFields:
        try:
            newFields["sex"] = Sex(newFields["sex"])
        except ValueError:
            return makeErrorDict("Parameter `sex` must be either `male` or `female`", 400)

    if len(changedFields) == 0:
        return makeErrorDict("Nothing to change", 400)

    for field in changedFields:
        fieldValue = newFields[field]
        fieldType = humanFields[field].annotation

        if not isinstance(fieldValue, fieldType):
            return makeErrorDict(f'Field "{field}" expected type {fieldType} but received {type(fieldValue)}', 400)

        setattr(database[humanIndex], field, newFields[field])

    return makeItemDict(database[humanIndex])

def removeHuman(id: str) -> dict:
    humanIndex = getHumanIndex(id)

    if humanIndex is None:
        return makeErrorDict("Human not found", 404)

    global database

    del database[humanIndex]

    return {"success": True}

@app.post("/api/human")
async def api_addHuman(human: Human) -> dict:
    return makeItemDict(addHuman(human))

@app.get("/api/human")
async def api_getHuman(id: Optional[str] = None) -> dict:
    if id is None:
        return makeItemsDict(database)

    human = getHuman(id)

    if human is None:
        raise HTTPException(404, "Human not found")

    return makeItemDict(human)

@app.put("/api/human")
async def api_updateHuman(id: str, newFields: dict) -> dict:
    newFields.pop("id", None)

    updateResult = updateHuman(id, **newFields)

    if "error" in updateResult:
        raise HTTPException(updateResult["error"]["http"]["statusCode"], updateResult["error"]["detail"])

    return updateResult

@app.delete("/api/human")
async def api_removeHuman(id: str) -> dict:
    removeResult = removeHuman(id)

    if "error" in removeResult:
        raise HTTPException(removeResult["error"]["http"]["statusCode"], removeResult["error"]["detail"])

    return removeResult

def main() -> None:
    pass # use the run_web.cmd file to run web

if __name__ == "__main__":
    main()

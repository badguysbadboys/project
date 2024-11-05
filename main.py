import dataclasses
from enum import Enum
from uuid import uuid4
from typing import Optional

database = []

class NotFound(Exception):
    ...

class Sex(Enum):
    Male = 0
    Female = 1

@dataclasses.dataclass
class Human:
    id: str = dataclasses.field(default_factory=lambda: uuid4().hex, init=False)

    lastName: str
    firstName: str

    height: float
    weight: float

    age: int

    sex: Sex

    middleName: str = str()

    def __post_init__(self) -> None:
        for field in dataclasses.fields(self):
            self.verifyFieldType(field, getattr(self, field.name))

    @staticmethod
    def verifyFieldType(field, fieldValue) -> None:
        fieldType = field.type

        if not isinstance(fieldValue, fieldType):
            raise TypeError(f'"{field.name}" expected type {fieldType} but received {type(fieldValue)}')

def addHuman(human: Human) -> Human:
    global database

    database.append(human)

def getHumanIndex(id: str) -> Optional[int]:
    for i in range(len(database)):
        if database[i].id == id:
            return i

    return None

def getHuman(id: str) -> Optional[Human]:
    humanIndex = getHumanIndex(id)

    return None if humanIndex is None else database[humanIndex]

def updateHuman(id: str, **newFields) -> None:
    humanIndex = getHumanIndex(id)

    if humanIndex is None:
        raise NotFound(f'Human with id "{id}" was not found')

    global database

    human = database[humanIndex]

    changedFields = {field: newFields[field.name] for field in filter(lambda field: field.name != "id", dataclasses.fields(human)) if field.name in newFields and getattr(human, field.name) != newFields[field.name]} if len(newFields) > 0 else {}

    if len(changedFields) == 0:
        raise ValueError("No fields to change")

    for field, fieldValue in changedFields.items():
        Human.verifyFieldType(field, fieldValue)

        setattr(database[humanIndex], field.name, fieldValue)

def removeHuman(id: str) -> None:
    humanIndex = getHumanIndex(id)

    if humanIndex is None:
        raise NotFound(f'Human with id "{id}" was not found')

    global database

    del database[humanIndex]

def main() -> None:
    pass

if __name__ == "__main__":
    main()

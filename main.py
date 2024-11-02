from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Sex(Enum):
    Male = 0
    Female = 1

@dataclass
class Human:
    lastName: str
    firstName: str

    height: float
    weight: float

    age: int

    sex: Sex

    middleName: str = str()

    def __post_init__(self) -> None:
        for fieldName, fieldType in self.__annotations__.items():
            fieldValue = self.__dict__[fieldName]

            if not isinstance(fieldValue, fieldType):
                raise TypeError(f'"{fieldName}": expected type {fieldType} but received {type(fieldValue)}')

def main() -> None:
    ...

if __name__ == "__main__":
    main()

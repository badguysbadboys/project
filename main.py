import dataclasses
from enum import Enum
from uuid import uuid4

database = []

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
            fieldName = field.name
            fieldType = field.type

            fieldValue = self.__dict__[fieldName]

            if not isinstance(fieldValue, fieldType):
                raise TypeError(f'"{fieldName}" expected type {fieldType} but received {type(fieldValue)}')

def main() -> None:
    pass

if __name__ == "__main__":
    main()

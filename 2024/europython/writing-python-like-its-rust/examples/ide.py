import dataclasses

from beartype import beartype


@dataclasses.dataclass
class Visitor:
    name: str
    age: int


@beartype
def get_visitor(name: str):
    pass


a = (1, 2)
print(a[2])

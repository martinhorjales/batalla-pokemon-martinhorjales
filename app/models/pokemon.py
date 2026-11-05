from dataclasses import dataclass

@dataclass
class Pokemon:
    height: int
    id: int
    name: str
    stats: list
    sprites: dict
    types: list
    weight: int
    moves: list
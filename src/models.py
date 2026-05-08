from dataclasses import dataclass


Position = tuple[int, int]


@dataclass(frozen=True)
class Item:
    name: str
    symbol: str
    position: Position
    value: int


@dataclass(frozen=True)
class Candidate:
    item: Item
    path: list[Position]
    cost: int

    @property
    def ratio(self) -> float:
        if self.cost == 0:
            return float("inf")
        return self.item.value / self.cost


@dataclass
class StepResult:
    item: Item
    path: list[Position]
    cost: int
    energy_left: int
    score: int
    ratio: float


@dataclass
class ManualMoveResult:
    moved: bool
    position: Position
    energy_left: int
    score: int
    collected_item: Item | None = None
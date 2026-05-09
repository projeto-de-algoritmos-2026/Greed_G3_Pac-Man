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
    path_items: list[Item]
    value: int

    @property
    def ratio(self) -> float:
        if self.cost == 0:
            return float("inf")
        return self.value / self.cost


@dataclass
class StepResult:
    item: Item
    path: list[Position]
    cost: int
    energy_left: int
    score: int
    ratio: float
    collected_items: list[Item]
    value_gained: int
    combo_bonus: int

@dataclass
class ManualMoveResult:
    moved: bool
    position: Position
    energy_left: int
    score: int
    collected_item: Item | None = None

    combo_bonus: int = 0


@dataclass(frozen=True)
class PlannedStep:
    target: Item
    path: list[Position]
    collected_items: list[Item]
    value_gained: int
    cost: int
    energy_after: int


@dataclass(frozen=True)
class OptimalPlan:
    score: int
    steps: list[PlannedStep]
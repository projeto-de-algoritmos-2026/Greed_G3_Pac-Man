from src.grid import Grid
from src.models import Candidate, Item, Position


def build_candidates(
    grid: Grid,
    current_position: Position,
    items: dict[Position, Item],
    energy_left: int,
) -> list[Candidate]:
    candidates: list[Candidate] = []

    for item in items.values():
        path = grid.shortest_path(current_position, item.position)
        if path is None:
            continue

        cost = len(path) - 1
        if cost <= energy_left:
            candidates.append(Candidate(item=item, path=path, cost=cost))

    return candidates


def choose_best_candidate(candidates: list[Candidate]) -> Candidate | None:
    if not candidates:
        return None

    return max(
        candidates,
        key=lambda candidate: (
            candidate.ratio,
            candidate.item.value,
            -candidate.cost,
            candidate.item.name,
        ),
    )
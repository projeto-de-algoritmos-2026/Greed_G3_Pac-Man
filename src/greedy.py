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
            path_items = [items[position] for position in path[1:] if position in items]
            value = sum(path_item.value for path_item in path_items)
            candidates.append(
                Candidate(
                    item=item,
                    path=path,
                    cost=cost,
                    path_items=path_items,
                    value=value,
                )
            )

    return candidates


def choose_best_candidate(candidates: list[Candidate]) -> Candidate | None:
    if not candidates:
        return None

    return max(
        candidates,
        key=lambda candidate: (
            candidate.ratio,
            candidate.value,
            -candidate.cost,
            candidate.item.name,
        ),
    )
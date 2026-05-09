from src.config import FRUIT_COMBO_BONUS, FRUIT_COMBO_MAX_MOVES, FRUIT_SYMBOLS
from src.grid import Grid
from src.models import Candidate, Item, Position


def build_candidates(
    grid: Grid,
    current_position: Position,
    items: dict[Position, Item],
    energy_left: int,
    moves_used: int = 0,
    last_fruit_move: int | None = None,
) -> list[Candidate]:
    candidates: list[Candidate] = []

    for item in items.values():
        path = grid.shortest_path(current_position, item.position)
        if path is None:
            continue

        cost = len(path) - 1
        if cost <= energy_left:
            path_items = [items[position] for position in path[1:] if position in items]
            value = path_value(path, items, moves_used, last_fruit_move)
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


def path_value(
    path: list[Position],
    items: dict[Position, Item],
    moves_used: int,
    last_fruit_move: int | None,
) -> int:
    value = 0
    current_last_fruit_move = last_fruit_move

    for step_index, position in enumerate(path[1:], start=1):
        item = items.get(position)
        if item is None:
            continue

        value += item.value
        if item.symbol in FRUIT_SYMBOLS:
            collection_move = moves_used + step_index
            if (
                current_last_fruit_move is not None
                and collection_move - current_last_fruit_move <= FRUIT_COMBO_MAX_MOVES
            ):
                value += FRUIT_COMBO_BONUS
            current_last_fruit_move = collection_move

    return value

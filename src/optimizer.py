from functools import lru_cache

from src.config import (
    FRUIT_COMBO_BONUS,
    FRUIT_COMBO_MAX_MOVES,
    FRUIT_SYMBOLS,
    VICTORY_ENERGY_BONUS,
)
from src.grid import Grid
from src.models import Item, OptimalPlan, PlannedStep, Position


def find_best_plan(
    grid: Grid,
    current_position: Position,
    remaining_items: dict[Position, Item],
    energy_left: int,
    moves_used: int,
    last_fruit_move: int | None,
) -> OptimalPlan:
    item_by_position = dict(remaining_items)
    shortest_paths: dict[tuple[Position, Position], list[Position] | None] = {}

    def get_path(start: Position, goal: Position) -> list[Position] | None:
        key = (start, goal)
        if key not in shortest_paths:
            shortest_paths[key] = grid.shortest_path(start, goal)
        return shortest_paths[key]

    def simulate_path(
        path: list[Position],
        remaining_positions: tuple[Position, ...],
        current_energy: int,
        current_last_fruit_move: int | None,
    ) -> tuple[int, int, tuple[Position, ...], int | None, list[Item]]:
        remaining_set = set(remaining_positions)
        collected_items: list[Item] = []
        gained_score = 0
        combo_last_fruit_move = current_last_fruit_move
        current_moves_used = moves_used + (energy_left - current_energy)

        for step_index, position in enumerate(path[1:], start=1):
            if position not in remaining_set:
                continue

            item = item_by_position[position]
            collection_move = current_moves_used + step_index
            item_score = item.value

            if item.symbol in FRUIT_SYMBOLS:
                if (
                    combo_last_fruit_move is not None
                    and collection_move - combo_last_fruit_move <= FRUIT_COMBO_MAX_MOVES
                ):
                    item_score += FRUIT_COMBO_BONUS
                combo_last_fruit_move = collection_move

            gained_score += item_score
            collected_items.append(item)
            remaining_set.remove(position)

        return (
            gained_score,
            current_energy - (len(path) - 1),
            tuple(sorted(remaining_set)),
            combo_last_fruit_move,
            collected_items,
        )

    @lru_cache(maxsize=None)
    def search(
        position: Position,
        remaining_positions: tuple[Position, ...],
        current_energy: int,
        current_last_fruit_move: int | None,
    ) -> tuple[int, tuple[PlannedStep, ...]]:
        if not remaining_positions:
            return current_energy * VICTORY_ENERGY_BONUS, ()

        best_score = -1
        best_steps: tuple[PlannedStep, ...] = ()

        for target_position in remaining_positions:
            path = get_path(position, target_position)
            if path is None:
                continue

            cost = len(path) - 1
            if cost > current_energy:
                continue

            (
                gained_score,
                next_energy,
                next_remaining_positions,
                next_last_fruit_move,
                collected_items,
            ) = simulate_path(path, remaining_positions, current_energy, current_last_fruit_move)

            future_score, future_steps = search(
                target_position,
                next_remaining_positions,
                next_energy,
                next_last_fruit_move,
            )
            total_score = gained_score + future_score

            if total_score > best_score:
                best_score = total_score
                best_steps = (
                    PlannedStep(
                        target=item_by_position[target_position],
                        path=path,
                        collected_items=collected_items,
                        value_gained=gained_score,
                        cost=cost,
                        energy_after=next_energy,
                    ),
                    *future_steps,
                )

        if best_score < 0:
            return 0, ()

        return best_score, best_steps

    score, steps = search(
        current_position,
        tuple(sorted(remaining_items)),
        energy_left,
        last_fruit_move,
    )
    return OptimalPlan(score=score, steps=list(steps))
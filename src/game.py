from src.config import (
    FRUIT_COMBO_BONUS,
    FRUIT_COMBO_MAX_MOVES,
    FRUIT_SYMBOLS,
    VICTORY_ENERGY_BONUS,
)
from src.greedy import build_candidates, choose_best_candidate
from src.grid import Grid
from src.models import Candidate, Item, ManualMoveResult, OptimalPlan, Position, StepResult
from src.optimizer import find_best_plan


class Game:
    def __init__(self, rows: list[str], initial_energy: int) -> None:
        self.grid = Grid(rows)
        self.initial_energy = initial_energy
        self.energy_left = initial_energy
        self.score = 0
        self.position: Position = self.grid.start
        self.remaining_items = dict(self.grid.items)
        self.history: list[StepResult] = []
        self.last_fruit_move: int | None = None

    def candidates(self) -> list[Candidate]:
        return build_candidates(
            self.grid,
            self.position,
            self.remaining_items,
            self.energy_left,
            self.moves_used,
            self.last_fruit_move,
        )

    def best_candidate(self) -> Candidate | None:
        return choose_best_candidate(self.candidates())

    def step(self) -> StepResult | None:
        best = self.best_candidate()

        if best is None:
            return None

        collected_items, value_gained, combo_bonus = self._collect_items_on_path(best.path)
        self.energy_left -= best.cost
        self.score += value_gained
        self.position = best.item.position

        result = StepResult(
            item=best.item,
            path=best.path,
            cost=best.cost,
            energy_left=self.energy_left,
            score=self.score,
            ratio=best.ratio,
            collected_items=collected_items,
            value_gained=value_gained,
            combo_bonus=combo_bonus,
        )
        self.history.append(result)
        return result

    def step_best_score(self) -> StepResult | None:
        plan = self.best_score_plan()
        if not plan.steps:
            return None

        next_step = plan.steps[0]
        return self.execute_path(next_step.path, next_step.target)

    def execute_path(self, path: list[Position], target: Item | None = None) -> StepResult | None:
        if len(path) < 2:
            return None

        cost = len(path) - 1
        if cost > self.energy_left:
            return None

        target_item = target or self.remaining_items.get(path[-1])
        if target_item is None:
            return None

        collected_items, value_gained, combo_bonus = self._collect_items_on_path(path)
        self.energy_left -= cost
        self.score += value_gained
        self.position = path[-1]

        ratio = value_gained / cost if cost else float("inf")
        result = StepResult(
            item=target_item,
            path=path,
            cost=cost,
            energy_left=self.energy_left,
            score=self.score,
            ratio=ratio,
            collected_items=collected_items,
            value_gained=value_gained,
            combo_bonus=combo_bonus,
        )
        self.history.append(result)
        return result

    def best_score_plan(self) -> OptimalPlan:
        return find_best_plan(
            self.grid,
            self.position,
            self.remaining_items,
            self.energy_left,
            self.moves_used,
            self.last_fruit_move,
        )

    def run_best_score_plan(self) -> OptimalPlan:
        plan = self.best_score_plan()
        for planned_step in plan.steps:
            self.execute_path(planned_step.path, planned_step.target)
        return plan

    def move_player(self, row_delta: int, col_delta: int) -> ManualMoveResult:
        if self.energy_left <= 0:
            return ManualMoveResult(False, self.position, self.energy_left, self.score)

        row, col = self.position
        next_position = (row + row_delta, col + col_delta)

        if not self.grid.is_walkable(next_position):
            return ManualMoveResult(False, self.position, self.energy_left, self.score)

        self.position = next_position
        self.energy_left -= 1
        collected_item = self.remaining_items.pop(self.position, None)
        combo_bonus = 0

        if collected_item is not None:
            combo_bonus = self._combo_bonus_for(collected_item, self.moves_used)
            self.score += collected_item.value + combo_bonus

        return ManualMoveResult(
            True,
            self.position,
            self.energy_left,
            self.score,
            collected_item,
            combo_bonus,
        )

    @property
    def moves_used(self) -> int:
        return self.initial_energy - self.energy_left

    def victory_bonus(self) -> int:
        if self.remaining_items:
            return 0
        return self.energy_left * VICTORY_ENERGY_BONUS

    def final_score(self) -> int:
        return self.score + self.victory_bonus()

    def collected_count(self) -> int:
        return len(self.grid.items) - len(self.remaining_items)

    def _collect_items_on_path(self, path: list[Position]) -> tuple[list, int, int]:
        collected_items = []
        value_gained = 0
        combo_bonus = 0
        moves_before_path = self.moves_used

        for step_index, position in enumerate(path[1:], start=1):
            collected_item = self.remaining_items.pop(position, None)
            if collected_item is None:
                continue

            item_combo_bonus = self._combo_bonus_for(
                collected_item,
                moves_before_path + step_index,
            )
            collected_items.append(collected_item)
            combo_bonus += item_combo_bonus
            value_gained += collected_item.value + item_combo_bonus

        return collected_items, value_gained, combo_bonus

    def _combo_bonus_for(self, item, collection_move: int) -> int:
        if item.symbol not in FRUIT_SYMBOLS:
            return 0

        bonus = 0
        if (
            self.last_fruit_move is not None
            and collection_move - self.last_fruit_move <= FRUIT_COMBO_MAX_MOVES
        ):
            bonus = FRUIT_COMBO_BONUS

        self.last_fruit_move = collection_move
        return bonus

    def is_finished(self) -> bool:
        return self.energy_left <= 0 or self.best_candidate() is None

    def solve(self) -> list[StepResult]:
        while self.step() is not None:
            pass
        return self.history

    def run(self) -> None:
        print("Pac-Man Greedy Knapsack")
        print("=" * 27)
        print(f"Energia inicial: {self.initial_energy}")
        print(f"Itens disponíveis: {len(self.remaining_items)}")
        print()
        print("Mapa inicial:")
        print(self.grid.render(self.position, self.remaining_items))
        print()

        round_number = 1
        while True:
            result = self.step_best_score()
            if result is None:
                break

            print(f"Rodada {round_number}")
            collected = ", ".join(
                f"{item.name} ({item.symbol})" for item in result.collected_items
            )
            print(
                f"Coletado(s): {collected} | "
                f"valor={result.value_gained} | custo={result.cost} | "
                f"valor/custo={result.ratio:.2f}"
            )
            if result.combo_bonus:
                print(f"Bônus de combo de frutas: +{result.combo_bonus}")
            print(f"Pontuação: {result.score} | Energia restante: {result.energy_left}")
            print(self.grid.render(self.position, self.remaining_items, result.path))
            print()
            round_number += 1

        print("Resultado final")
        print("=" * 15)
        print(f"Pontuação dos itens e combos: {self.score}")
        print(f"Bônus de energia na vitória: {self.victory_bonus()}")
        print(f"Pontuação final: {self.final_score()}")
        print(f"Energia usada: {self.initial_energy - self.energy_left}")
        print(f"Energia restante: {self.energy_left}")
        print(f"Itens coletados: {self.collected_count()}")
        print(f"Itens ignorados: {len(self.remaining_items)}")

        if not self.remaining_items:
            print("Vitória: todos os itens foram coletados.")

        if self.remaining_items:
            print()
            print("Itens não coletados:")
            for item in self.remaining_items.values():
                print(f"- {item.name} ({item.symbol}) em {item.position}, valor={item.value}")

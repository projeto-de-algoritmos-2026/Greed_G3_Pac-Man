from src.greedy import build_candidates, choose_best_candidate
from src.grid import Grid
from src.models import Candidate, ManualMoveResult, Position, StepResult


class Game:
    def __init__(self, rows: list[str], initial_energy: int) -> None:
        self.grid = Grid(rows)
        self.initial_energy = initial_energy
        self.energy_left = initial_energy
        self.score = 0
        self.position: Position = self.grid.start
        self.remaining_items = dict(self.grid.items)
        self.history: list[StepResult] = []

    def candidates(self) -> list[Candidate]:
        return build_candidates(
            self.grid,
            self.position,
            self.remaining_items,
            self.energy_left,
        )
    
    def best_candidate(self) -> Candidate | None:
        return choose_best_candidate(self.candidates())

    def step(self) -> StepResult | None:
        best = self.best_candidate()

        if best is None:
            return None

        collected_items = []
        for item in best.path_items:
            collected_item = self.remaining_items.pop(item.position, None)
            if collected_item is not None:
                collected_items.append(collected_item)

        value_gained = sum(item.value for item in collected_items)
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
        )
        self.history.append(result)
        return result

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

        if collected_item is not None:
            self.score += collected_item.value

        return ManualMoveResult(
            True,
            self.position,
            self.energy_left,
            self.score,
            collected_item,
        )

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
            result = self.step()
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
            print(f"Pontuação: {result.score} | Energia restante: {result.energy_left}")
            print(self.grid.render(self.position, self.remaining_items, result.path))
            print()
            round_number += 1

        print("Resultado final")
        print("=" * 15)
        print(f"Pontuação total: {self.score}")
        print(f"Energia usada: {self.initial_energy - self.energy_left}")
        print(f"Energia restante: {self.energy_left}")
        collected_count = sum(len(result.collected_items) for result in self.history)
        print(f"Itens coletados: {collected_count}")
        print(f"Itens ignorados: {len(self.remaining_items)}")

        if not self.remaining_items:
            print("Vitória: todos os itens foram coletados.")

        if self.remaining_items:
            print()
            print("Itens não coletados:")
            for item in self.remaining_items.values():
                print(f"- {item.name} ({item.symbol}) em {item.position}, valor={item.value}")
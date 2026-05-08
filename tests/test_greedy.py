import unittest

from src.game import Game
from src.greedy import build_candidates, choose_best_candidate
from src.grid import Grid


class GreedyKnapsackTest(unittest.TestCase):
    def test_shortest_path_uses_grid_corridors(self) -> None:
        grid = Grid(
            [
                "#####",
                "#P  #",
                "### #",
                "# F #",
                "#####",
            ]
        )

        path = grid.shortest_path(grid.start, (3, 2))

        self.assertIsNotNone(path)
        self.assertEqual(len(path) - 1, 5)

    def test_choose_best_candidate_by_value_cost_ratio(self) -> None:
        grid = Grid(
            [
                "#######",
                "#P F O#",
                "#######",
            ]
        )
        candidates = build_candidates(grid, grid.start, grid.items, energy_left=10)

        best = choose_best_candidate(candidates)

        self.assertIsNotNone(best)
        self.assertEqual(best.item.symbol, "F")

    def test_game_stops_when_remaining_items_do_not_fit_energy(self) -> None:
        game = Game(
            [
                "#######",
                "#P   F#",
                "#######",
            ],
            initial_energy=2,
        )

        history = game.solve()

        self.assertEqual(history, [])
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.remaining_items), 1)


if __name__ == "__main__":
    unittest.main()
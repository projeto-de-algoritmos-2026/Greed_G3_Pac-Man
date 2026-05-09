import argparse

from src.config import DEFAULT_ENERGY
from src.game import Game
from src.maps import DEFAULT_MAP
from src.ui import run_gui


def main() -> None:
    parser = argparse.ArgumentParser(description="Pac-Man com estratégia gulosa Knapsack.")
    parser.add_argument(
        "--terminal",
        action="store_true",
        help="executa a versão textual automática no terminal",
    )
    parser.add_argument(
        "--best-score",
        action="store_true",
        help="executa a busca pela maior pontuação possível no terminal",
    )
    args = parser.parse_args()

    if args.best_score:
        game = Game(DEFAULT_MAP, initial_energy=DEFAULT_ENERGY)
        plan = game.run_best_score_plan()
        print("Pac-Man Maior Pontuação")
        print("======================")
        print(f"Passes planejados: {len(plan.steps)}")
        print(f"Pontuação dos itens e combos: {game.score}")
        print(f"Bônus de energia na vitória: {game.victory_bonus()}")
        print(f"Pontuação final: {game.final_score()}")
        print(f"Energia restante: {game.energy_left}")
    elif args.terminal:
        game = Game(DEFAULT_MAP, initial_energy=DEFAULT_ENERGY)
        game.run()
    else:
        run_gui()

if __name__ == "__main__":
    main()
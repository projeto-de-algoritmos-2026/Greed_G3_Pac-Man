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
    args = parser.parse_args()

    if args.terminal:
        game = Game(DEFAULT_MAP, initial_energy=DEFAULT_ENERGY)
        game.run()
    else:
        run_gui()

if __name__ == "__main__":
    main()
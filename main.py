from src.game import Game
from src.maps import DEFAULT_MAP


def main() -> None:
    game = Game(DEFAULT_MAP, initial_energy=35)
    game.run()


if __name__ == "__main__":
    main()
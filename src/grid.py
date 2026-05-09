from collections import deque

from src.maps import ITEM_VALUES
from src.models import Item, Position

WALL = "#"
PLAYER = "P"


class Grid:
    def __init__(self, rows: list[str]) -> None:
        if not rows:
            raise ValueError("O mapa precisa ter ao menos uma linha.")

        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("Todas as linhas do mapa precisam ter o mesmo tamanho.")

        self.rows = [list(row) for row in rows]
        self.height = len(rows)
        self.width = width
        self.start = self._find_player()
        self.items = self._find_items()

    def _find_player(self) -> Position:
        players: list[Position] = []
        for row_index, row in enumerate(self.rows):
            for col_index, symbol in enumerate(row):
                if symbol == PLAYER:
                    players.append((row_index, col_index))

        if len(players) != 1:
            raise ValueError("O mapa precisa ter exatamente um jogador inicial 'P'.")
        return players[0]

    def _find_items(self) -> dict[Position, Item]:
        items: dict[Position, Item] = {}
        for row_index, row in enumerate(self.rows):
            for col_index, symbol in enumerate(row):
                if symbol in ITEM_VALUES:
                    name, value = ITEM_VALUES[symbol]
                    position = (row_index, col_index)
                    items[position] = Item(name, symbol, position, value)
        return items

    def is_walkable(self, position: Position) -> bool:
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width and self.rows[row][col] != WALL

    def neighbors(self, position: Position) -> list[Position]:
        row, col = position
        possible = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return [neighbor for neighbor in possible if self.is_walkable(neighbor)]

    def shortest_path(self, start: Position, goal: Position) -> list[Position] | None:
        queue: deque[Position] = deque([start])
        previous: dict[Position, Position | None] = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                return self._rebuild_path(previous, goal)

            for neighbor in self.neighbors(current):
                if neighbor not in previous:
                    previous[neighbor] = current
                    queue.append(neighbor)

        return None

    def _rebuild_path(
        self,
        previous: dict[Position, Position | None],
        goal: Position,
    ) -> list[Position]:
        path: list[Position] = []
        current: Position | None = goal
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path

    def render(
        self,
        player: Position,
        remaining_items: dict[Position, Item],
        highlighted_path: list[Position] | None = None,
    ) -> str:
        path_positions = set(highlighted_path or [])
        output = [row[:] for row in self.rows]

        for row_index in range(self.height):
            for col_index in range(self.width):
                position = (row_index, col_index)
                if output[row_index][col_index] != WALL:
                    output[row_index][col_index] = " "
                if position in path_positions and position != player:
                    output[row_index][col_index] = "*"

        for item in remaining_items.values():
            output[item.position[0]][item.position[1]] = item.symbol

        output[player[0]][player[1]] = PLAYER
        return "\n".join("".join(row) for row in output)

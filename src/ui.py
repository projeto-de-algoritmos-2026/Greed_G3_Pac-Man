from __future__ import annotations

import tkinter as tk
from tkinter import font

from src.game import Game
from src.maps import DEFAULT_MAP
from src.models import Candidate, ManualMoveResult, Position, StepResult


CELL_SIZE = 42
PANEL_WIDTH = 310
TOP_PADDING = 12
SIDE_PADDING = 12
INITIAL_ENERGY = 35

COLORS = {
    "background": "#101820",
    "panel": "#18212c",
    "wall": "#214f93",
    "floor": "#0f1720",
    "grid": "#1f2a36",
    "path": "#f2b84b",
    "player": "#ffd43b",
    "point": "#f8f8f2",
    "power": "#66d9ef",
    "fruit": "#ff5c8a",
    "cherry": "#bd7cff",
    "text": "#f8f8f2",
    "muted": "#b8c2cc",
    "success": "#7bd88f",
    "warning": "#ffcc66",
}

ITEM_COLORS = {
    ".": COLORS["point"],
    "O": COLORS["power"],
    "F": COLORS["fruit"],
    "C": COLORS["cherry"],
}

ITEM_LABELS = {
    ".": ".",
    "O": "O",
    "F": "F",
    "C": "C",
}


class PacManApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.game = Game(DEFAULT_MAP, INITIAL_ENERGY)
        self.mode = "Manual"
        self.auto_running = False
        self.last_path: list[Position] = []
        self.message = "Use setas ou WASD para jogar. O modo automático usa valor/custo."

        self.title_font = font.Font(family="Segoe UI", size=17, weight="bold")
        self.body_font = font.Font(family="Segoe UI", size=10)
        self.small_font = font.Font(family="Segoe UI", size=9)
        self.grid_font = font.Font(family="Consolas", size=14, weight="bold")

        width = self.game.grid.width * CELL_SIZE + PANEL_WIDTH + SIDE_PADDING * 3
        height = self.game.grid.height * CELL_SIZE + TOP_PADDING * 2

        root.title("Greed G3 Pac-Man")
        root.configure(bg=COLORS["background"])
        root.geometry(f"{width}x{height}")
        root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=self.game.grid.width * CELL_SIZE,
            height=self.game.grid.height * CELL_SIZE,
            bg=COLORS["floor"],
            highlightthickness=0,
        )
        self.canvas.place(x=SIDE_PADDING, y=TOP_PADDING)

        self.panel = tk.Frame(root, bg=COLORS["panel"])
        self.panel.place(
            x=self.game.grid.width * CELL_SIZE + SIDE_PADDING * 2,
            y=TOP_PADDING,
            width=PANEL_WIDTH,
            height=self.game.grid.height * CELL_SIZE,
        )

        self._build_panel()
        self._bind_keys()
        self.render()

    def _build_panel(self) -> None:
        tk.Label(
            self.panel,
            text="Pac-Man Knapsack",
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=self.title_font,
        ).pack(anchor="w", padx=18, pady=(18, 4))

        tk.Label(
            self.panel,
            text="Greed: maior valor / custo",
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=self.body_font,
        ).pack(anchor="w", padx=18, pady=(0, 16))

        self.status_label = tk.Label(
            self.panel,
            justify="left",
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=self.body_font,
        )
        self.status_label.pack(anchor="w", padx=18, pady=(0, 14))

        self.best_label = tk.Label(
            self.panel,
            justify="left",
            wraplength=PANEL_WIDTH - 36,
            bg=COLORS["panel"],
            fg=COLORS["warning"],
            font=self.body_font,
        )
        self.best_label.pack(anchor="w", padx=18, pady=(0, 14))

        button_frame = tk.Frame(self.panel, bg=COLORS["panel"])
        button_frame.pack(fill="x", padx=18, pady=(0, 16))

        self.manual_button = tk.Button(
            button_frame,
            text="Modo manual",
            command=self.set_manual_mode,
            font=self.body_font,
            relief="flat",
        )
        self.manual_button.pack(fill="x", pady=3)

        self.auto_step_button = tk.Button(
            button_frame,
            text="Auto step",
            command=self.auto_step,
            font=self.body_font,
            relief="flat",
        )
        self.auto_step_button.pack(fill="x", pady=3)

        self.auto_play_button = tk.Button(
            button_frame,
            text="Auto play",
            command=self.toggle_auto_play,
            font=self.body_font,
            relief="flat",
        )
        self.auto_play_button.pack(fill="x", pady=3)

        self.reset_button = tk.Button(
            button_frame,
            text="Resetar",
            command=self.reset,
            font=self.body_font,
            relief="flat",
        )
        self.reset_button.pack(fill="x", pady=3)

        self.message_label = tk.Label(
            self.panel,
            justify="left",
            wraplength=PANEL_WIDTH - 36,
            bg=COLORS["panel"],
            fg=COLORS["success"],
            font=self.small_font,
        )
        self.message_label.pack(anchor="w", padx=18, pady=(0, 14))

        legend = (
            "Legenda\n"
            "P  Pac-Man\n"
            ".  ponto comum\n"
            "O  power-up\n"
            "F  fruta\n"
            "C  cereja\n"
            "*  rota do auto"
        )
        tk.Label(
            self.panel,
            text=legend,
            justify="left",
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=self.small_font,
        ).pack(anchor="w", padx=18, pady=(8, 0))

    def _bind_keys(self) -> None:
        bindings = {
            "<Up>": (-1, 0),
            "<Down>": (1, 0),
            "<Left>": (0, -1),
            "<Right>": (0, 1),
            "w": (-1, 0),
            "W": (-1, 0),
            "s": (1, 0),
            "S": (1, 0),
            "a": (0, -1),
            "A": (0, -1),
            "d": (0, 1),
            "D": (0, 1),
        }

        for key, delta in bindings.items():
            self.root.bind(key, lambda event, move=delta: self.handle_manual_move(move))

        self.root.bind("<space>", lambda event: self.auto_step())
        self.root.bind("r", lambda event: self.reset())
        self.root.bind("R", lambda event: self.reset())

    def handle_manual_move(self, delta: tuple[int, int]) -> None:
        if self.auto_running:
            return

        self.mode = "Manual"
        self.last_path = []
        result = self.game.move_player(*delta)
        self.message = self._manual_message(result)
        self.render()

    def _manual_message(self, result: ManualMoveResult) -> str:
        if not result.moved:
            if self.game.energy_left <= 0:
                return "Sem energia. Use Resetar para jogar novamente."
            return "Movimento bloqueado por parede ou limite do mapa."

        if result.collected_item is None:
            return "Movimento realizado. Nenhum item coletado nesta célula."

        return (
            f"Coletado manualmente: {result.collected_item.name} "
            f"(+{result.collected_item.value} pontos)."
        )

    def set_manual_mode(self) -> None:
        self.auto_running = False
        self.mode = "Manual"
        self.last_path = []
        self.message = "Modo manual ativo. Use setas ou WASD."
        self.render()

    def auto_step(self) -> None:
        self.auto_running = False
        self.mode = "Automático"
        result = self.game.step()

        if result is None:
            self.last_path = []
            self.message = "Nenhum item restante cabe na energia disponível."
        else:
            self.last_path = result.path
            self.message = self._auto_message(result)

        self.render()

    def toggle_auto_play(self) -> None:
        self.auto_running = not self.auto_running
        self.mode = "Automático"
        self.auto_play_button.configure(text="Pausar auto" if self.auto_running else "Auto play")
        self.message = "Auto play em execução." if self.auto_running else "Auto play pausado."
        self.render()

        if self.auto_running:
            self.root.after(650, self.auto_loop)

    def auto_loop(self) -> None:
        if not self.auto_running:
            return

        result = self.game.step()
        if result is None:
            self.auto_running = False
            self.auto_play_button.configure(text="Auto play")
            self.message = "Auto play finalizado: não há item possível com a energia atual."
            self.last_path = []
            self.render()
            return

        self.last_path = result.path
        self.message = self._auto_message(result)
        self.render()
        self.root.after(650, self.auto_loop)

    def _auto_message(self, result: StepResult) -> str:
        return (
            f"Auto coletou {result.item.name}: valor={result.item.value}, "
            f"custo={result.cost}, razão={result.ratio:.2f}."
        )

    def reset(self) -> None:
        self.auto_running = False
        self.auto_play_button.configure(text="Auto play")
        self.game = Game(DEFAULT_MAP, INITIAL_ENERGY)
        self.mode = "Manual"
        self.last_path = []
        self.message = "Jogo resetado. Use setas/WASD ou rode o modo automático."
        self.render()

    def render(self) -> None:
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_path()
        self._draw_items()
        self._draw_player()
        self._update_panel()

    def _draw_grid(self) -> None:
        for row_index in range(self.game.grid.height):
            for col_index in range(self.game.grid.width):
                x1 = col_index * CELL_SIZE
                y1 = row_index * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                symbol = self.game.grid.rows[row_index][col_index]
                fill = COLORS["wall"] if symbol == "#" else COLORS["floor"]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=COLORS["grid"])

    def _draw_path(self) -> None:
        for row, col in self.last_path:
            if (row, col) == self.game.position:
                continue
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill=COLORS["path"], outline="")

    def _draw_items(self) -> None:
        for item in self.game.remaining_items.values():
            row, col = item.position
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            color = ITEM_COLORS[item.symbol]

            if item.symbol == ".":
                self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline="")
            else:
                self.canvas.create_oval(x - 14, y - 14, x + 14, y + 14, fill=color, outline="")
                self.canvas.create_text(
                    x,
                    y,
                    text=ITEM_LABELS[item.symbol],
                    fill=COLORS["background"],
                    font=self.grid_font,
                )

    def _draw_player(self) -> None:
        row, col = self.game.position
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        self.canvas.create_oval(x - 16, y - 16, x + 16, y + 16, fill=COLORS["player"], outline="")
        self.canvas.create_polygon(
            x,
            y,
            x + 17,
            y - 8,
            x + 17,
            y + 8,
            fill=COLORS["floor"],
            outline="",
        )

    def _update_panel(self) -> None:
        self.status_label.configure(
            text=(
                f"Modo: {self.mode}\n"
                f"Pontuação: {self.game.score}\n"
                f"Energia: {self.game.energy_left}/{self.game.initial_energy}\n"
                f"Itens restantes: {len(self.game.remaining_items)}\n"
                f"Coletas automáticas: {len(self.game.history)}"
            )
        )

        best = self.game.best_candidate()
        self.best_label.configure(text=self._best_candidate_text(best))
        self.message_label.configure(text=self.message)

    def _best_candidate_text(self, candidate: Candidate | None) -> str:
        if candidate is None:
            return "Melhor escolha gulosa: nenhuma opção cabe na energia atual."

        return (
            "Melhor escolha gulosa\n"
            f"{candidate.item.name} ({candidate.item.symbol})\n"
            f"valor={candidate.item.value} | custo={candidate.cost}\n"
            f"valor/custo={candidate.ratio:.2f}"
        )


def run_gui() -> None:
    root = tk.Tk()
    PacManApp(root)
    root.mainloop()
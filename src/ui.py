from __future__ import annotations

import tkinter as tk
from tkinter import font

from src.config import DEFAULT_ENERGY
from src.game import Game
from src.maps import DEFAULT_MAP
from src.models import ManualMoveResult, PlannedStep, Position, StepResult


CELL_SIZE = 42
PANEL_WIDTH = 310
PANEL_HEIGHT = 560
TOP_PADDING = 12
SIDE_PADDING = 12

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
        self.game = Game(DEFAULT_MAP, DEFAULT_ENERGY)
        self.mode = "Manual"
        self.auto_running = False
        self.last_path: list[Position] = []
        self.message = "Use setas ou WASD para jogar. O modo automático busca maior pontuação."

        self.title_font = font.Font(family="Segoe UI", size=17, weight="bold")
        self.body_font = font.Font(family="Segoe UI", size=10)
        self.small_font = font.Font(family="Segoe UI", size=9)
        self.grid_font = font.Font(family="Consolas", size=14, weight="bold")

        width = self.game.grid.width * CELL_SIZE + PANEL_WIDTH + SIDE_PADDING * 3
        height = max(self.game.grid.height * CELL_SIZE, PANEL_HEIGHT) + TOP_PADDING * 2

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
            height=PANEL_HEIGHT,
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
            text="Automático: maior pontuação",
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
        self.status_label.pack(anchor="w", padx=18, pady=(0, 10))

        self.best_label = tk.Label(
            self.panel,
            justify="left",
            wraplength=PANEL_WIDTH - 36,
            bg=COLORS["panel"],
            fg=COLORS["warning"],
            font=self.body_font,
        )
        self.best_label.pack(anchor="w", padx=18, pady=(0, 8))

        self.message_label = tk.Label(
            self.panel,
            justify="left",
            wraplength=PANEL_WIDTH - 36,
            bg=COLORS["panel"],
            fg=COLORS["success"],
            font=self.small_font,
        )
        self.message_label.pack(anchor="w", padx=18, pady=(0, 8))

        button_frame = tk.Frame(self.panel, bg=COLORS["panel"])
        button_frame.place(x=18, y=PANEL_HEIGHT - 180, width=PANEL_WIDTH - 36, height=166)

        self.manual_button = tk.Button(
            button_frame,
            text="Modo manual",
            command=self.set_manual_mode,
            font=self.body_font,
            relief="flat",
        )
        self.manual_button.pack(fill="x", ipady=3, pady=(0, 7))

        self.auto_step_button = tk.Button(
            button_frame,
            text="Passe automático",
            command=self.auto_step,
            font=self.body_font,
            relief="flat",
        )
        self.auto_step_button.pack(fill="x", ipady=3, pady=(0, 7))

        self.auto_play_button = tk.Button(
            button_frame,
            text="Jogo automático",
            command=self.toggle_auto_play,
            font=self.body_font,
            relief="flat",
        )
        self.auto_play_button.pack(fill="x", ipady=3, pady=(0, 7))

        self.reset_button = tk.Button(
            button_frame,
            text="Resetar",
            command=self.reset,
            font=self.body_font,
            relief="flat",
        )
        self.reset_button.pack(fill="x", ipady=3)

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
        self.message = self._finished_message() if not self.game.remaining_items else self._manual_message(result)
        self.render()

    def _manual_message(self, result: ManualMoveResult) -> str:
        if not result.moved:
            if self.game.energy_left <= 0:
                return "Sem energia. Use Resetar para jogar novamente."
            return "Movimento bloqueado por parede ou limite do mapa."

        if result.collected_item is None:
            return "Movimento realizado. Nenhum item coletado nesta célula."

        combo = f" Combo de fruta: +{result.combo_bonus}." if result.combo_bonus else ""
        return (
            f"Coletado manualmente: {result.collected_item.name} "
            f"(+{result.collected_item.value} pontos).{combo}"
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
        result = self.game.step_best_score()

        if result is None:
            self.last_path = []
            self.message = self._finished_message()
        else:
            self.last_path = result.path
            self.message = self._finished_message() if not self.game.remaining_items else self._auto_message(result)

        self.render()

    def toggle_auto_play(self) -> None:
        self.auto_running = not self.auto_running
        self.mode = "Automático"
        self.auto_play_button.configure(
            text="Pausar automático" if self.auto_running else "Jogo automático"
        )
        self.message = (
            "Jogo automático em execução."
            if self.auto_running
            else "Jogo automático pausado."
        )
        self.render()

        if self.auto_running:
            self.root.after(650, self.auto_loop)

    def auto_loop(self) -> None:
        if not self.auto_running:
            return

        result = self.game.step_best_score()
        if result is None:
            self.auto_running = False
            self.auto_play_button.configure(text="Jogo automático")
            self.message = self._finished_message()
            self.last_path = []
            self.render()
            return

        self.last_path = result.path
        self.message = self._finished_message() if not self.game.remaining_items else self._auto_message(result)
        self.render()
        self.root.after(650, self.auto_loop)

    def _auto_message(self, result: StepResult) -> str:
        collected = ", ".join(item.name for item in result.collected_items)
        combo = f" Combo de frutas: +{result.combo_bonus}." if result.combo_bonus else ""
        return (
            f"Automático coletou {collected}: valor={result.value_gained}, "
            f"custo={result.cost}, razão={result.ratio:.2f}.{combo}"
        )

    def _finished_message(self) -> str:
        if not self.game.remaining_items:
            return "Vitória! Todos os itens foram coletados."
        return "Fim de jogo: nenhum item restante cabe na energia disponível."

    def reset(self) -> None:
        self.auto_running = False
        self.auto_play_button.configure(text="Jogo automático")
        self.game = Game(DEFAULT_MAP, DEFAULT_ENERGY)
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
                f"Pontos: {self.game.score}\n"
                f"Bônus vitória: {self.game.victory_bonus()}\n"
                f"Pontuação final: {self.game.final_score()}\n"
                f"Energia: {self.game.energy_left}/{self.game.initial_energy}\n"
                f"Itens restantes: {len(self.game.remaining_items)}\n"
                f"Passes automáticos: {len(self.game.history)}"
            )
        )

        plan = self.game.best_score_plan()
        next_step = plan.steps[0] if plan.steps else None
        self.best_label.configure(text=self._best_plan_text(next_step, plan.score))
        self.message_label.configure(text=self.message)

    def _best_plan_text(self, step: PlannedStep | None, final_score: int) -> str:
        if step is None:
            return "Próximo passe otimizado: nenhuma rota cabe na energia atual."

        collected = ", ".join(item.symbol for item in step.collected_items)

        return (
            "Próximo passe otimizado\n"
            f"Destino: {step.target.name} ({step.target.symbol})\n"
            f"Coleta na rota: {collected}\n"
            f"valor={step.value_gained} | custo={step.cost}\n"
            f"pontuação final prevista={self.game.score + final_score}"
        )


def run_gui() -> None:
    root = tk.Tk()
    PacManApp(root)
    root.mainloop()

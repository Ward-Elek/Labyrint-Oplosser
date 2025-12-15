"""Debug viewer that overlays learned Q-values on the maze grid."""

import threading

import numpy as np
import pygame
from PIL import Image, ImageDraw, ImageFont

from convert import Feasibility
from draw import cell_side, draw_image, line_thickness, margin
from learn import Agent
from live_training_viewer import prompt_for_value
from maze import Maze


class QValueDebugViewer:
    """Render a static maze annotated with per-cell Q-values."""

    def __init__(self, maze, feasibility, agent, title: str = "Q-value debug viewer"):
        self.maze = maze
        self.feasibility = feasibility
        self.agent = agent
        self.title = title
        self.screen = None
        self.background = None
        self.clock = None
        self.zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 3.0
        self.base_width = None
        self.base_height = None
        self.maze_width = None
        self.maze_height = None
        self.static_background = None
        self.font = None

        self._init_display()

    def _init_display(self):
        pygame.init()
        self.maze_width, self.maze_height = (
            margin + cell_side * dim for dim in self.maze.maze_grid.shape
        )
        self.base_width = self.maze_width
        self.base_height = self.maze_height
        self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.static_background = self._render_static_background()
        self.background = self.static_background

        try:
            self.font = ImageFont.truetype("Arial Unicode.ttf", 18)
        except OSError:
            self.font = ImageFont.load_default()

    def _render_static_background(self):
        img = Image.new("RGB", (self.base_width, self.base_height), (255, 255, 255))
        drawer = ImageDraw.Draw(img)
        draw_image(drawer, self.maze.maze_grid)
        self._highlight_start_and_end(drawer)
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def _render_q_overlay(self):
        img = Image.new("RGBA", (self.base_width, self.base_height), (0, 0, 0, 0))
        drawer = ImageDraw.Draw(img)
        self._annotate_q_values(drawer)
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def _highlight_start_and_end(self, drawer: ImageDraw.ImageDraw):
        padding = line_thickness
        for cell, color in (
            (self._find_cell_with_status("Start"), (0, 255, 0)),
            (self._find_cell_with_status("End"), (255, 0, 0)),
        ):
            if cell is None:
                continue

            center_x, center_y = self._cell_center(cell)
            half_side = cell_side / 2
            drawer.rectangle(
                (
                    center_x - half_side + padding,
                    center_y - half_side + padding,
                    center_x + half_side - padding,
                    center_y + half_side - padding,
                ),
                fill=color,
            )

    def _find_cell_with_status(self, status: str):
        for cell in self.maze.maze_grid.flatten():
            if getattr(cell, "status", None) == status:
                return cell
        return None

    def _cell_center(self, cell):
        x = margin + line_thickness + cell.x * cell_side
        y = margin + line_thickness + cell.y * cell_side
        return int(x), int(y)

    def _annotate_q_values(self, drawer: ImageDraw.ImageDraw):
        state_to_indices = {
            int(state): (i, j)
            for i, row in enumerate(self.feasibility.numbered_grid)
            for j, state in enumerate(row)
        }

        for state, (x_idx, y_idx) in state_to_indices.items():
            cell = self.maze.maze_grid[x_idx, y_idx]
            center_x, center_y = self._cell_center(cell)
            q_values = self.agent.Q[state]
            mask = self.feasibility.F_matrix[state] == 1
            filtered = q_values[mask]
            value = float(np.max(filtered)) if filtered.size else 0.0
            label = f"{value:.1f}"
            text_box = drawer.textbbox((0, 0), label, font=self.font)
            text_width = text_box[2] - text_box[0]
            text_height = text_box[3] - text_box[1]
            drawer.text(
                (
                    center_x - text_width / 2,
                    center_y - text_height / 2,
                ),
                label,
                fill=(0, 0, 0),
                font=self.font,
            )

    def _scaled_dimensions(self):
        width = int(self.base_width * self.zoom)
        height = int(self.base_height * self.zoom)
        return width, height

    def _compose_frame(self):
        overlay = self._render_q_overlay()
        composed = self.static_background.copy()
        composed.blit(overlay, (0, 0))
        return composed

    def _blit_scaled_surface(self):
        self.background = self._compose_frame()
        width, height = self._scaled_dimensions()
        scaled_background = pygame.transform.smoothscale(self.background, (width, height))
        offset_x = (self.screen.get_width() - width) // 2
        offset_y = (self.screen.get_height() - height) // 2
        self.screen.fill((255, 255, 255))
        self.screen.blit(scaled_background, (offset_x, offset_y))

    def _change_zoom(self, delta):
        self.zoom = min(self.max_zoom, max(self.min_zoom, self.zoom + delta))

    def run(self, fps: int = 30, completion_event: threading.Event | None = None):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    self._change_zoom(0.1 * event.y)
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self._change_zoom(0.1)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self._change_zoom(-0.1)

            self._blit_scaled_surface()
            pygame.display.flip()
            self.clock.tick(fps)

            if completion_event and completion_event.is_set():
                pygame.display.set_caption(f"{self.title} (training complete)")

        pygame.quit()


def train_agent_with_inputs():
    """Train an agent using interactive prompts and return it with the maze."""

    dimensions = prompt_for_value(
        "Enter maze dimensions separated by a space (e.g. 4 4): ",
        lambda raw: [int(v) for v in raw.split()],
        lambda vals: len(vals) == 2 and all(v > 0 for v in vals),
        "Please provide two positive integers separated by a space.",
    )
    dimension1, dimension2 = dimensions

    start_coords = prompt_for_value(
        "Enter x and y coordinates of the maze start separated by a space: ",
        lambda raw: [int(v) for v in raw.split()],
        lambda vals: len(vals) == 2 and 0 <= vals[0] < dimension1 and 0 <= vals[1] < dimension2,
        "Start coordinates should be inside the maze. Numbering is zero-based.",
    )
    start_x, start_y = start_coords

    gamma = prompt_for_value(
        "Enter the gamma value (0, 1]: ",
        float,
        lambda val: 0 < val <= 1,
        "Gamma should be a number between 0 and 1.",
    )

    lrn_rate = prompt_for_value(
        "Enter the learning rate value (0, 1]: ",
        float,
        lambda val: 0 < val <= 1,
        "Learning rate should be a number between 0 and 1.",
    )

    max_epochs = 1000

    maze = Maze(dimension1, dimension2, [start_x, start_y])
    feasibility = Feasibility(maze)
    agent = Agent(feasibility, gamma, lrn_rate, maze, start_x, start_y)
    training_done = threading.Event()

    def training_task():
        agent.train(
            feasibility.F_matrix,
            max_epochs,
            record_episodes=False,
            record_q_values=False,
        )
        training_done.set()

    viewer = QValueDebugViewer(maze, feasibility, agent)
    training_thread = threading.Thread(target=training_task, daemon=True)
    training_thread.start()

    viewer.run(completion_event=training_done)
    training_thread.join()

    return maze, feasibility, agent


def main():
    train_agent_with_inputs()


if __name__ == "__main__":
    main()

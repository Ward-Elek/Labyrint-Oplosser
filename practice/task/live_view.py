"""Real-time Pygame visualization for the training process.

The viewer listens for state updates emitted by the agent's training loop
and renders the agent's current position inside the maze as those updates
arrive.
"""

import queue
from typing import Optional

import numpy as np
import pygame
from PIL import Image, ImageDraw

from draw import cell_side, draw_image, line_thickness, margin


class LiveMazeViewer:
    """Display live agent movement using Pygame."""

    def __init__(self, maze, feasibility, title: str = "Live Maze Training"):
        self.maze = maze
        self.feasibility = feasibility
        self.title = title
        self.update_queue: "queue.Queue[int]" = queue.Queue()
        self.current_state: Optional[int] = None
        self.running = False
        self.screen = None
        self.background = None
        self.clock = None
        self.trail_surface = None
        self.previous_cell = None
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        self.base_width = None
        self.base_height = None
        self.state_to_indices = {
            int(state): (i, j)
            for i, row in enumerate(self.feasibility.numbered_grid)
            for j, state in enumerate(row)
        }
        self.visit_counts = np.zeros_like(self.feasibility.numbered_grid, dtype=int)
        self.max_visit_count = 1

        self._init_display()

    def _init_display(self):
        pygame.init()
        self.base_width, self.base_height = (
            margin + cell_side * dim for dim in self.maze.maze_grid.shape
        )
        self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.background = self._render_background()
        self.trail_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

    def _render_background(self):
        img = Image.new("RGB", (self.base_width, self.base_height), (255, 255, 255))
        drawer = ImageDraw.Draw(img)
        draw_image(drawer, self.maze.maze_grid)
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def enqueue_state(self, state: int):
        """Add a new state update to the rendering queue."""

        self.update_queue.put(state)

    def _state_to_cell(self, state: int):
        idx_x, idx_y = self.state_to_indices[state]
        return self.maze.maze_grid[idx_x, idx_y]

    def _cell_center(self, cell):
        x = margin + line_thickness + cell.x * cell_side
        y = margin + line_thickness + cell.y * cell_side
        return int(x), int(y)

    def _drain_updates(self):
        while True:
            try:
                state = self.update_queue.get_nowait()
            except queue.Empty:
                break

            self.current_state = state
            cell = self._state_to_cell(state)
            self._increment_visit(state)
            self._draw_trail(state, cell)

    def _increment_visit(self, state):
        idx_x, idx_y = self.state_to_indices[state]
        self.visit_counts[idx_x, idx_y] += 1
        self.max_visit_count = max(self.max_visit_count, self.visit_counts[idx_x, idx_y])

    def _visit_color(self, state):
        idx_x, idx_y = self.state_to_indices[state]
        count = self.visit_counts[idx_x, idx_y]
        ratio = count / self.max_visit_count
        start_color = np.array([255, 220, 220])
        end_color = np.array([180, 0, 0])
        color = start_color + ratio * (end_color - start_color)
        return tuple(int(channel) for channel in color)

    def _draw_trail(self, state, cell):
        color = self._visit_color(state)
        current_center = self._cell_center(cell)
        if self.previous_cell is not None:
            pygame.draw.line(
                self.trail_surface,
                color,
                self._cell_center(self.previous_cell),
                current_center,
                max(1, int(line_thickness / 2)),
            )

        pygame.draw.circle(self.trail_surface, color, current_center, int(cell_side / 4))
        self.previous_cell = cell

    def _scaled_dimensions(self):
        width = int(self.base_width * self.zoom)
        height = int(self.base_height * self.zoom)
        return width, height

    def _scale_point(self, point):
        width, height = self._scaled_dimensions()
        offset_x = (self.screen.get_width() - width) // 2
        offset_y = (self.screen.get_height() - height) // 2
        return int(point[0] * self.zoom + offset_x), int(point[1] * self.zoom + offset_y)

    def _draw_agent(self):
        if self.current_state is None:
            return

        cell = self._state_to_cell(self.current_state)
        center = self._scale_point(self._cell_center(cell))
        pygame.draw.circle(
            self.screen,
            (0, 0, 255),
            center,
            max(1, int((cell_side / 3) * self.zoom)),
        )

    def _blit_scaled_surfaces(self):
        width, height = self._scaled_dimensions()
        scaled_background = pygame.transform.smoothscale(self.background, (width, height))
        scaled_trail = pygame.transform.smoothscale(self.trail_surface, (width, height))

        offset_x = (self.screen.get_width() - width) // 2
        offset_y = (self.screen.get_height() - height) // 2

        self.screen.fill((255, 255, 255))
        self.screen.blit(scaled_background, (offset_x, offset_y))
        self.screen.blit(scaled_trail, (offset_x, offset_y))

    def _change_zoom(self, delta):
        self.zoom = min(self.max_zoom, max(self.min_zoom, self.zoom + delta))

    def run(self, completion_event: Optional["threading.Event"] = None, fps: int = 30):
        """Start the rendering loop.

        Parameters
        ----------
        completion_event: threading.Event | None
            Optional event that signals when training has finished. When the
            event is set and no new updates are pending, the loop exits.
        fps: int
            Maximum frames per second for the draw loop.
        """

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEWHEEL:
                    self._change_zoom(0.1 * event.y)
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self._change_zoom(0.1)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self._change_zoom(-0.1)

            self._drain_updates()
            self._blit_scaled_surfaces()
            self._draw_agent()
            pygame.display.flip()

            if completion_event and completion_event.is_set() and self.update_queue.empty():
                self.running = False

            self.clock.tick(fps)

        pygame.quit()

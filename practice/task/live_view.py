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

        self._init_display()

    def _init_display(self):
        pygame.init()
        width, height = (margin + cell_side * dim for dim in self.maze.maze_grid.shape)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.background = self._render_background()

    def _render_background(self):
        width, height = (margin + cell_side * dim for dim in self.maze.maze_grid.shape)
        img = Image.new("RGB", (width, height), (255, 255, 255))
        drawer = ImageDraw.Draw(img)
        draw_image(drawer, self.maze.maze_grid)
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def enqueue_state(self, state: int):
        """Add a new state update to the rendering queue."""

        self.update_queue.put(state)

    def _state_to_cell(self, state: int):
        idx_x = np.where(self.feasibility.numbered_grid == state)[0][0]
        idx_y = np.where(self.feasibility.numbered_grid == state)[1][0]
        return self.maze.maze_grid[idx_x, idx_y]

    def _cell_center(self, cell):
        x = margin + line_thickness + cell.x * cell_side
        y = margin + line_thickness + cell.y * cell_side
        return int(x), int(y)

    def _drain_updates(self):
        while True:
            try:
                self.current_state = self.update_queue.get_nowait()
            except queue.Empty:
                break

    def _draw_agent(self):
        if self.current_state is None:
            return

        cell = self._state_to_cell(self.current_state)
        pygame.draw.circle(self.screen, (0, 0, 255), self._cell_center(cell), int(cell_side / 3))

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

            self._drain_updates()
            self.screen.blit(self.background, (0, 0))
            self._draw_agent()
            pygame.display.flip()

            if completion_event and completion_event.is_set() and self.update_queue.empty():
                self.running = False

            self.clock.tick(fps)

        pygame.quit()

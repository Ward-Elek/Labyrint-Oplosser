"""Real-time Pygame visualization for the training process.

The viewer listens for state updates emitted by the agent's training loop
and renders the agent's current position inside the maze as those updates
arrive.
"""

import datetime
import queue
from pathlib import Path
from typing import Optional

import numpy as np
import pygame
from PIL import Image, ImageDraw

from callback_protocol import RESET_SIGNAL
from draw import cell_side, draw_image, line_thickness, margin


class LiveMazeViewer:
    """Display live agent movement using Pygame."""

    def __init__(
        self,
        maze,
        feasibility,
        title: str = "Live Maze Training",
        metrics_window: int = 100,
    ):
        self.maze = maze
        self.feasibility = feasibility
        self.title = title
        self.update_queue: "queue.Queue[object]" = queue.Queue()
        self.metrics_queue: "queue.Queue[object]" = queue.Queue()
        self.current_state: Optional[int] = None
        self.running = False
        self.screen = None
        self.background = None
        self.clock = None
        self.trail_surface = None
        self.metrics_surface = None
        self.previous_cell = None
        self.zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 3.0
        self.base_width = None
        self.base_height = None
        self.maze_width = None
        self.maze_height = None
        self.metrics_width = 220
        self.metrics_visible = True
        self.metrics_window = metrics_window
        self.state_to_indices = {
            int(state): (i, j)
            for i, row in enumerate(self.feasibility.numbered_grid)
            for j, state in enumerate(row)
        }
        self.visit_counts = np.zeros_like(self.feasibility.numbered_grid, dtype=int)
        self.max_visit_count = 1
        self.solved_path_states = None
        self.solved_path_surface = None
        self.metric_series: dict[str, list[float]] = {}
        self.metric_colors = [
            (52, 152, 219),
            (46, 204, 113),
            (231, 76, 60),
            (155, 89, 182),
        ]
        self.metric_font = None

        self._init_display()

    def _init_display(self):
        pygame.init()
        self.maze_width, self.maze_height = (
            margin + cell_side * dim for dim in self.maze.maze_grid.shape
        )
        self.base_width = self.maze_width + self.metrics_width
        self.base_height = self.maze_height
        self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.background = self._render_background()
        self.trail_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.metrics_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.metric_font = pygame.font.SysFont(None, 14)

    def _render_background(self):
        img = Image.new("RGB", (self.base_width, self.base_height), (255, 255, 255))
        drawer = ImageDraw.Draw(img)
        draw_image(drawer, self.maze.maze_grid)
        self._highlight_start_and_end(drawer)
        drawer.rectangle(
            (
                self.maze_width,
                0,
                self.base_width - 1,
                self.base_height - 1,
            ),
            fill=(245, 245, 245),
            outline=(200, 200, 200),
        )
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

    def enqueue_state(self, state):
        """Add a new state update (or control signal) to the rendering queue."""

        self.update_queue.put(state)

    def enqueue_metrics(self, metrics):
        """Add a metrics update to the metrics rendering queue."""

        self.metrics_queue.put(metrics)

    def reset_trail(self, clear_surface: bool = False):
        """Clear the stored trail between episodes.

        Parameters
        ----------
        clear_surface: bool
            When True, removes any previously drawn trail markers.
        """

        self.previous_cell = None
        self.current_state = None
        if clear_surface and self.trail_surface:
            self.trail_surface.fill((0, 0, 0, 0))

    def set_solved_path(self, path_states):
        """Store the solved path states for later rendering.

        The actual drawing occurs in the render loop to keep all Pygame
        operations on the same thread.
        """

        self.solved_path_states = path_states

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

            if state == RESET_SIGNAL:
                self.reset_trail()
                continue

            self.current_state = state
            cell = self._state_to_cell(state)
            self._increment_visit(state)
            self._draw_trail(state, cell)

    def _drain_metrics(self):
        updated = False

        while True:
            try:
                metrics = self.metrics_queue.get_nowait()
            except queue.Empty:
                break

            updated = True
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    if isinstance(value, (int, float, np.floating)):
                        self.metric_series.setdefault(str(key), []).append(float(value))
            elif isinstance(metrics, (int, float, np.floating)):
                self.metric_series.setdefault("value", []).append(float(metrics))

        if updated:
            self._redraw_metrics_surface()

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
        scaled_metrics = None
        if self.metrics_surface and self.metrics_visible:
            scaled_metrics = pygame.transform.smoothscale(self.metrics_surface, (width, height))

        offset_x = (self.screen.get_width() - width) // 2
        offset_y = (self.screen.get_height() - height) // 2

        self.screen.fill((255, 255, 255))
        self.screen.blit(scaled_background, (offset_x, offset_y))
        self.screen.blit(scaled_trail, (offset_x, offset_y))
        if self.solved_path_surface:
            scaled_solution = pygame.transform.smoothscale(self.solved_path_surface, (width, height))
            self.screen.blit(scaled_solution, (offset_x, offset_y))
        if scaled_metrics:
            self.screen.blit(scaled_metrics, (offset_x, offset_y))

    def _change_zoom(self, delta):
        self.zoom = min(self.max_zoom, max(self.min_zoom, self.zoom + delta))

    def _redraw_metrics_surface(self):
        if not self.metrics_surface:
            return

        self.metrics_surface.fill((0, 0, 0, 0))
        if not self.metrics_visible:
            return

        panel_x = self.maze_width
        panel_rect = pygame.Rect(panel_x, 0, self.metrics_width, self.base_height)
        pygame.draw.rect(self.metrics_surface, (250, 250, 250), panel_rect)
        pygame.draw.rect(self.metrics_surface, (200, 200, 200), panel_rect, 1)

        if not self.metric_series:
            return

        padding = 12
        gap = 8
        plot_rect = panel_rect.inflate(-2 * padding, -2 * padding)

        metric_items = list(self.metric_series.items())
        num_plots = len(metric_items)

        if num_plots == 0:
            return

        subplot_height = 0
        if num_plots:
            available_height = plot_rect.height - gap * (num_plots - 1)
            subplot_height = max(20, available_height // num_plots)

        y_cursor = plot_rect.top
        for idx, (name, series) in enumerate(metric_items):
            subplot_rect = pygame.Rect(plot_rect.left, y_cursor, plot_rect.width, subplot_height)
            y_cursor += subplot_height + gap

            data = series[-self.metrics_window :]
            if not data:
                continue

            if len(data) > subplot_rect.width:
                data = data[-subplot_rect.width :]

            min_value = min(data)
            max_value = max(data)
            value_range = max(max_value - min_value, 1e-5)

            color = self.metric_colors[idx % len(self.metric_colors)]
            points = []
            for i, value in enumerate(data):
                x = subplot_rect.left + int(i * (subplot_rect.width - 1) / max(1, len(data) - 1))
                y_ratio = (value - min_value) / value_range
                y = subplot_rect.bottom - int(y_ratio * (subplot_rect.height - 1))
                points.append((x, y))

            pygame.draw.rect(self.metrics_surface, (220, 220, 220), subplot_rect, 1)
            if len(points) == 1:
                pygame.draw.circle(self.metrics_surface, color, points[0], 2)
            else:
                pygame.draw.lines(self.metrics_surface, color, False, points, 2)

            if self.metric_font:
                label_surface = self.metric_font.render(str(name), True, (80, 80, 80))
                label_pos = (subplot_rect.left + 4, subplot_rect.top + 2)
                self.metrics_surface.blit(label_surface, label_pos)

    def _toggle_metrics(self):
        self.metrics_visible = not self.metrics_visible
        self._redraw_metrics_surface()

    def _ensure_solved_path_surface(self):
        """Render a green overlay for the solved path once available."""

        if self.solved_path_surface is not None or not self.solved_path_states:
            return

        solution_surface = pygame.Surface((self.base_width, self.base_height), pygame.SRCALPHA)
        path_cells = [self._state_to_cell(state) for state in self.solved_path_states if state in self.state_to_indices]

        if len(path_cells) < 2:
            return

        points = [self._cell_center(cell) for cell in path_cells]
        pygame.draw.lines(solution_surface, (0, 180, 0), False, points, max(2, int(line_thickness)))
        for center in points:
            pygame.draw.circle(solution_surface, (0, 200, 0), center, int(cell_side / 5))

        self.solved_path_surface = solution_surface

    def _save_final_images(self):
        """Persist the current maze and metrics views to disk."""

        if not self.screen:
            return

        base_dir = Path(__file__).resolve().parents[2] / "Media"
        base_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Refresh the composed surface before saving.
        self._blit_scaled_surfaces()
        self._draw_agent()

        maze_path = base_dir / f"maze_view_{timestamp}.png"
        pygame.image.save(self.screen, maze_path)

        if self.solved_path_surface:
            solved_surface = pygame.Surface((self.base_width, self.base_height), pygame.SRCALPHA)
            solved_surface.blit(self.background, (0, 0))
            solved_surface.blit(self.solved_path_surface, (0, 0))
            solved_path = base_dir / f"solved_maze_{timestamp}.png"
            pygame.image.save(solved_surface, solved_path)

        if self.metrics_surface:
            metrics_panel = pygame.Surface((self.base_width, self.base_height), pygame.SRCALPHA)
            metrics_panel.blit(self.metrics_surface, (0, 0))
            metrics_path = base_dir / f"metrics_panel_{timestamp}.png"
            pygame.image.save(metrics_panel, metrics_path)

    def run(self, completion_event: Optional["threading.Event"] = None, fps: int = 30):
        """Start the rendering loop.

        Parameters
        ----------
        completion_event: threading.Event | None
            Optional event that signals when training has finished. The viewer
            remains open until the user closes the window.
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
                    elif event.key == pygame.K_m:
                        self._toggle_metrics()

            self._drain_updates()
            self._drain_metrics()
            self._ensure_solved_path_surface()
            self._blit_scaled_surfaces()
            self._draw_agent()
            pygame.display.flip()

            self.clock.tick(fps)

        self._save_final_images()
        pygame.quit()

import os
import json


class Level:
    """Lädt ein Level aus der Datenbank und stellt Grid-Infos bereit."""

    # Zellentypen
    FREE  = 0
    WALL  = 1
    HOLE  = 2
    GOAL  = 3
    START = 4

    def __init__(self, level_name, grid):
        self.name = level_name
        self.grid = grid               # 2D-Liste [[int, ...], ...]
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.start_col, self.start_row = self._find_start()

    def _find_start(self):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == self.START:
                    return c, r
        return 1, 1  # Fallback

    def get_cell(self, col, row):
        """Gibt den Zellentyp zurück. -1 bei ungültigen Koordinaten."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return self.WALL  # Außerhalb = Wand

    def cell_rect(self, col, row, cell_size):
        """Gibt (x, y, w, h) in Pixel für eine Zelle zurück.
        Ursprung ist unten links (Kivy-Koordinatensystem)."""
        x = col * cell_size
        y = (self.rows - 1 - row) * cell_size
        return (x, y, cell_size, cell_size)

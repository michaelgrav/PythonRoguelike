import numpy as np # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height

        # Create a 2d array, filled with the same values. It Basically fills self.tiles with floor tiles
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[30:33, 22] = tile_types.wall

    # Makes sure the player doesn't leave the map
    def in_bounds(self, x: int, y: int) -> bool:
        """Return true if x and y are inside of the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
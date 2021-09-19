from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)

        # Create a 2d array, filled with the same values. It Basically fills self.tiles with floor tiles
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        # Tiles the player can currently see
        self.visible = np.full((width, height), fill_value=False, order="F")
        # Tiles the player has seen before
        self.explored = np.full((width, height), fill_value=False, order="F")

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                # If entity is found that blocks movement and occupies location_x and location_y, it returns that Entity
                return entity

        return None

    # Makes sure the player doesn't leave the map
    def in_bounds(self, x: int, y: int) -> bool:
        """Return true if x and y are inside of the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map

        If a tile is in the "visible" array, then draw it with the "light" colors
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors
        Otherwise, the default is "SHROUD"
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            # This line will check if the tile is either visible, then explored
            condlist=[self.visible, self.explored],
            # If visible, use "light", if explored use "dark"
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            # If neither use "SHROUD"
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print enemies that are in FOV
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

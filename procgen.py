from typing import Tuple

from game_map import GameMap
import tile_types

class RectangularRoom:
    # Takes coordinates of the top left corner and computes the bottom right
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    # Essentially a read-only variable for our RectangularRoom class, it describes the center of the room
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    # Returns two slices which represent the inner portion of the room
    # This is the part we will be digging out for our room
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
        # The function has +1s because if the rooms are next to each other
        # there needs to be an extra space for the wall


def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    return dungeon

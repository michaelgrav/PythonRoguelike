from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types


if TYPE_CHECKING:
    from entity import Entity


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

    def intersects(self, other: RectangularRoom) -> bool:
        """Returns true if this room overlaps with another Rectangular room"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


# The method takes two arguments (two tuples of two integers) and returns an iterator or a Tuple of two ints
def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # Move horizontally and then vertically
        corner_x, corner_y = x2, y1
    else:
        # Move vertically and then horizontally
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,  # Max rooms allowed in the dungeon
        room_min_size: int,  # Min size on one room
        room_max_size: int,  # Max size of one room
        map_width: int,  # Width of the GameMap
        map_height: int,  # Height of the GameMap
        player: Entity,  # The player, so we know where to place it
) -> GameMap:
    """Generate a new dungeon map"""
    dungeon = GameMap(map_width, map_height)

    # Running list of all rooms
    rooms: List[RectangularRoom] = []

    # Iterate from 0 to max_rooms - 1
    # We dont know how many rooms this will generate, but we know it cant exceed an amount
    for r in range(max_rooms):
        # Get a random size for the room
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        # Get a random pair of x and y coord to try and place the room
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Go through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, go to the next attempt (we get rid of this one)
        # If there are no intersections this room is valid

        # Dig out this rooms inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # This is the first room, where the player starts
            player.x, player.y = new_room.center
        else:  # All rooms after the first one
            # Dig a tunnel between this room and the one before it
            for x, y, in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list
        rooms.append(new_room)

    return dungeon


from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap


class Engine:
    """
        entities is a set of entities
        event_handler handles events
        player is the player entity
    """
    game_map: GameMap

    def __init__(self, player: Entity):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')

    def update_fov(self) -> None:
        """Recompute the visible area based on the players POV"""
        self.game_map.visible[:] = compute_fov(
            # 2D numpy array, all non zero values area transparent. This is used to calculate FOV
            self.game_map.tiles["transparent"],

            # Origin point for the FOV (2D index)
            (self.player.x, self.player.y),

            # How far the FOV extends
            radius=8,
        )

        # If a tile is "visible" it should be added to "explored"
        # This line sets the explored array to include everything in the visible, plus what it had already
        self.game_map.explored |= self.game_map.visible

    # Handles drawing to the screen, iterate though self.entities and print them
    def render(self, console: Console, context: Context):
        self.game_map.render(console)

        context.present(console)

        console.clear()

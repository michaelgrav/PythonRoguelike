from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import  EventHandler


class Engine:
    """
        entities is a set of entities
        event_handler handles events
        player is the player entity
    """
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player

    # Enemies take their turns
    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

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

        console.print(
            x=1,
            y=47,
            string=f"HP {self.player.fighter.hp}/{self.player.fighter.max_hp}",
        )

        context.present(console)

        console.clear()

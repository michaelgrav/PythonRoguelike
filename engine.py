from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    """
        entities is a set of entities
        event_handler handles events
        player is the player entity
    """
    def __init__(self, entities: Set[Entity], event_handler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    # Pass the events into this so it can iterate through them
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()  # Update the FOV before the players next action

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

        for entity in self.entities:
            # Only print enemies that are in FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()


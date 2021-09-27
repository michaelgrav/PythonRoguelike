from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp  # Hit Points
        self._hp = hp
        self.defense = defense  # How much taken damage will be reduced
        self.power = power  # Raw attack power

    @property  # Getter method, just returns the hp
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))  # Hp will never be less than 0, and can't go higher than max
        if self._hp == 0 and self.parent.ai:  # if hp is 0, kill the entity
            self.die()

    def die(self) -> None:
        # Print out a message indicating the death of the enemy
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        # Set the entity’s character to “%” (most roguelikes use this for corpses)
        self.parent.char = "%"

        # Set its color to red
        self.parent.color = (191, 0, 0)

        # Set blocks_movement to False, so that the entities can walk over the corpse
        self.parent.blocks_movement = False

        # Remove the AI from the entity, so it’ll be marked as dead and won’t take any more turns
        self.parent.ai = None

        # Change the name to this
        self.parent.name = f"remains of {self.parent.name}"

        # Update the render order to reflect a dead body
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

    def heal(self, amount: int) -> int:
        """Restore a certain amount of HP, up to the maximum, and return the amount that was healed"""
        if self.hp == self.max_hp:  # If already at max health
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:  # If healing goes above max hp
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

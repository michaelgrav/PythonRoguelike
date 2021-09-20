from components.base_component import BaseComponent


class Fighter(BaseComponent):
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
        self._hp = max(0, max(value, self.max_hp))  # Hp will never be less than 0, and can't go higher than max

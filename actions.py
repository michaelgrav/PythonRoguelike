class Action:
    pass


# Subclass of action
class EscapeAction(Action):
    pass


# Subclass of action
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

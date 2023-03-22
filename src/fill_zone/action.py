from src.action import Action


class FillZoneAction(Action):
    def __init__(self, color: int):
        self._color = color

    def get_color(self) -> int:
        return self._color

    def __eq__(self, other):
        return other == self._color or (isinstance(other, FillZoneAction) and other._color == self._color)

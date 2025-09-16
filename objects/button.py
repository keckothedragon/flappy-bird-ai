from utils.base_object import BaseObject


class Button(BaseObject):
    def __init__(self, x, y, width, height, game_display, image, on_click):
        super().__init__(x, y, width, height, game_display, ignore_self=True)
        self.image = image
        self.on_click = on_click

    def draw(self) -> None:
        self.game_display.blit(self.image, (self.x, self.y))

    def update(self) -> None:
        super().update()

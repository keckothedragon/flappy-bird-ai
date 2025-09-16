from utils.base_object import BaseObject


class Score(BaseObject):
    def __init__(self, x, y, font, text_color, game_display):
        super().__init__(x, y, 0, 0, game_display)
        self.score = 0
        self.font = font
        self.text_color = text_color

    def increment(self) -> None:
        self.score += 1

    def get_score(self) -> int:
        return self.score

    def draw(self) -> None:
        text_surface = self.font.render(str(self.score), True, self.text_color)
        self.game_display.blit(text_surface, (self.x, self.y))

    def update(self) -> None:
        super().update()

    def reset(self) -> None:
        self.score = 0

    def __str__(self):
        return f"Score: {super().__str__()} {self.score}"

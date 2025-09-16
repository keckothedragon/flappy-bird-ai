from utils.base_object import BaseObject
from objects.button import Button
import pygame


class Menu(BaseObject):
    def __init__(self, x, y, width, height, game_display, image,
                 highscore: tuple[int, tuple[int, int], pygame.font, pygame.font], buttons=None):
        super().__init__(x, y, width, height, game_display)
        self.image = image
        if buttons is None:
            buttons = []
        self.buttons = buttons
        self.hidden = False
        self.highscore, self.highscore_position, self.highscore_text_font, self.highscore_number_font = highscore

    def draw(self) -> None:
        if self.hidden:
            return
        self.game_display.blit(self.image, (self.x, self.y))

        highscore_text = self.highscore_text_font.render(f"Highscore ", True, (0, 0, 0))
        highscore_number = self.highscore_number_font.render(f"{self.highscore}", True, (0, 0, 0))
        self.game_display.blit(highscore_text, self.highscore_position)
        if self.highscore >= 10:
            self.game_display.blit(highscore_number, (self.highscore_position[0],
                                                      self.highscore_position[1] + highscore_text.get_height()))
        else:
            self.game_display.blit(highscore_number, (self.highscore_position[0] + highscore_text.get_width(),
                                                      self.highscore_position[1]))

        for button in self.buttons:
            button.draw()

    def update(self) -> None:
        if self.hidden:
            return
        super().update()

    def add_button(self, button: Button) -> None:
        self.buttons.append(button)

    def hide(self) -> None:
        self.hidden = True

    def show(self) -> None:
        self.hidden = False

    def update_highscore(self, new_score: int) -> bool:
        if new_score > self.highscore:
            self.highscore = new_score
            return True
        return False

    def __str__(self):
        return f"Menu: {super().__str__()}"


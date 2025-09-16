from utils.base_object import BaseObject
from utils.movement import Movement
import pygame


class Floor(BaseObject):
    def __init__(self, y: int, height: int, game_display: pygame.display, image: pygame.image,
                 movement=Movement(-5, 0)):
        super().__init__(0, y, game_display.get_width(), height, game_display, movement)
        self.image = image

    def draw(self) -> None:
        self.game_display.blit(self.image, (self.x, self.y))

    def update(self) -> None:
        if self.x < -self.width:
            self.x = 0
        super().update()

    def check_collision(self, other: "BaseObject") -> bool:
        collision_y = False
        if self.y <= other.y + other.height <= self.y + self.height:
            collision_y = True
        return collision_y

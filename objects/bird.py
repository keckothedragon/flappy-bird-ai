from utils.movement import Movement
from utils.base_object import BaseObject
from utils.animated import Animated
import pygame
from copy import copy


class Bird(BaseObject):
    def __init__(self, x, y, width, height, jump_height, game_display, images: Animated or pygame.Surface = None):
        super().__init__(x, y, width, height, game_display, Movement(0, 0), bounds=None)
        self.jump_height = jump_height
        if isinstance(images, Animated) or images is None:
            self.images = images
        else:
            self.images = Animated([images], 1)
        self.start_images = copy(self.images)

    def jump(self) -> None:
        self.set_movement(Movement(0, -self.jump_height))

    def is_touching_ground(self) -> bool:
        return self.y == self.game_display.get_height() - self.height

    def draw(self) -> None:
        rotation = self.get_movement().get_delta_y() * -3
        if rotation < -90:
            rotation = -90
        elif rotation > 90:
            rotation = 90
        if self.images is not None:
            self.game_display.blit(pygame.transform.rotate(self.images.get_frame(), rotation), (self.x, self.y))
        else:
            super().draw()

    def update(self) -> None:
        self.images.update()
        self.set_movement(Movement(self.get_movement().delta_x, self.get_movement().get_delta_y() + 1))
        super().update()

    def reset(self) -> None:
        self.images = copy(self.start_images)
        super().reset()

    def crash(self) -> None:
        # stop on current frame
        self.images = Animated([self.images.get_frame()], 1)

    def __str__(self):
        return f"Bird: {super().__str__()} {self.get_movement()}"

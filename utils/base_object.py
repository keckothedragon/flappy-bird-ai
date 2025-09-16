from utils.movement import Movement
import pygame
import numpy as np


class BaseObject:
    child = []

    def __init__(self, x: int, y: int, width: int, height: int,
                 game_display: pygame.display, movement=Movement(0, 0),
                 bounds: tuple[tuple[int, int], tuple[int, int]] = None,
                 ignore_self: bool = False):
        if not ignore_self:
            self.__class__.child.append(self)
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = width
        self.height = height
        self.game_display = game_display
        self.movement = movement
        self.start_movement = movement
        self.bounds = bounds

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_movement(self) -> Movement:
        return self.movement

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def set_x(self, x: int) -> None:
        self.x = x

    def set_y(self, y: int) -> None:
        self.y = y

    def set_movement(self, movement: Movement) -> None:
        self.movement = movement

    def set_bounds_screen(self) -> None:
        self.bounds = ((0, self.game_display.get_width()), (0, self.game_display.get_height()))

    def set_bounds(self, bounds: tuple[tuple[int, int], tuple[int, int]]) -> None:
        self.bounds = bounds

    def draw(self) -> None:
        pygame.draw.rect(self.game_display, (0, 0, 0), (self.x, self.y, self.width, self.height))

    def update(self) -> None:
        self.x += self.movement.get_delta_x()
        self.y += self.movement.get_delta_y()
        if self.bounds is not None:
            x_bounds, y_bounds = self.bounds
            self.x = np.clip(self.x, x_bounds[0], x_bounds[1] - self.width)
            self.y = np.clip(self.y, y_bounds[0], y_bounds[1] - self.height)
        self.draw()

    def check_collision(self, other: "BaseObject") -> bool:
        collision_x = False
        collision_y = False
        if self.x < other.x < self.x + self.width:
            collision_x = True
        elif self.x < other.x + other.width < self.x + self.width:
            collision_x = True
        if self.y < other.y < self.y + self.height:
            collision_y = True
        elif self.y < other.y + other.height < self.y + self.height:
            collision_y = True
        return collision_x and collision_y

    def check_collision_position(self, x: int, y: int) -> bool:
        collision_x = False
        collision_y = False
        if self.x < x < self.x + self.width:
            collision_x = True
        if self.y < y < self.y + self.height:
            collision_y = True
        return collision_x and collision_y

    def reset(self) -> None:
        self.x = self.start_x
        self.y = self.start_y
        self.movement = self.start_movement

    @classmethod
    def update_all(cls) -> None:
        for child in cls.child:
            child.update()

    @classmethod
    def draw_all(cls) -> None:
        for child in cls.child:
            child.draw()

    @classmethod
    def reset_all(cls) -> None:
        for child in cls.child:
            child.reset()

    @classmethod
    def clear_all(cls) -> None:
        cls.child = []

    def __str__(self):
        return f"({self.x}, {self.y})"

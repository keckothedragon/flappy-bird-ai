import pygame
from utils.movement import Movement
from utils.base_object import BaseObject
from random import randint
from objects.score import Score


class Pipe(BaseObject):
    def __init__(self, width, gap_height, game_display, image: pygame.image, movement=Movement(-5, 0)):
        super().__init__(game_display.get_width(), 0, width, game_display.get_height(), game_display, movement)
        self.gap_height = gap_height
        self.gap_y = randint(120, game_display.get_height() - gap_height - 120)
        self.image = image
        self.score = None

    def link_score(self, score: Score):
        self.score = score

    def draw(self) -> None:
        # top pipe
        cropped = pygame.Surface((self.width, self.gap_y), pygame.SRCALPHA, 32)
        cropped = cropped.convert_alpha()
        cropped.blit(self.image, (0, 0), (0, 0, self.width, self.gap_y))
        self.game_display.blit(pygame.transform.flip(cropped, False, True), (self.x, self.y))

        # bottom pipe
        cropped = pygame.Surface((self.width, self.game_display.get_height() - self.gap_y - self.gap_height),
                                 pygame.SRCALPHA, 32)
        cropped = cropped.convert_alpha()
        cropped.blit(self.image, (0, 0), (0, 0, self.width, self.game_display.get_height()))
        self.game_display.blit(cropped, (self.x, self.gap_y + self.gap_height))

    def respawn(self) -> None:
        self.x = self.game_display.get_width()
        self.gap_y = randint(120, self.game_display.get_height() - self.gap_height - 120)
        if self.score is not None:
            self.score.increment()

    def update(self) -> None:
        if self.x < -self.width:
            self.respawn()
        super().update()

    def check_collision(self, other: "BaseObject") -> bool:
        collision_x = False
        top_pipe_collision_y = False
        bottom_pipe_collision_y = False
        if self.x < other.x < self.x + self.width:
            collision_x = True
        elif self.x < other.x + other.width < self.x + self.width:
            collision_x = True
        if self.y < other.y < self.y + self.gap_y:
            top_pipe_collision_y = True
        elif self.y < other.y + other.height < self.y + self.gap_y:
            top_pipe_collision_y = True
        if self.y + self.gap_y + self.gap_height < other.y < self.y + self.height:
            bottom_pipe_collision_y = True
        elif self.y + self.gap_y + self.gap_height < other.y + other.height < self.y + self.height:
            bottom_pipe_collision_y = True
        return collision_x and (top_pipe_collision_y or bottom_pipe_collision_y)

    def get_gap(self) -> pygame.rect.Rect:
        return pygame.rect.Rect(self.x, self.gap_y, self.width, self.gap_height)

    def __str__(self):
        return f"Pipe: {super().__str__()} {self.get_movement()}"

import pygame

from objects.bird import Bird
import constants
from utils.animated import Animated
import random


class DefaultBird(Bird):
    def __init__(self, game_display, bird_id=-1):
        super().__init__(constants.PLAYER_START_X, constants.PLAYER_START_Y,
                         constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT, constants.PLAYER_JUMP_HEIGHT, game_display,
                         Animated([pygame.image.load(image) for image in constants.PLAYER_IMAGES_PATH], 60, 4))
        self.set_bounds(((-100, constants.DISPLAY_WIDTH), (0, constants.DISPLAY_HEIGHT - constants.FLOOR_HEIGHT)))

        self.bird_id = bird_id

        self.replace_colors()

        self.kill_self = False

    def replace_colors(self):
        SRC_COLORS = [0xffc20e, 0xff0000, 0xff7e00]
        REPLACEMENT_COLORS = [
            0xffffff,
            0xffffff,
            0x000000,
            0x000000,
            0xaa00aa,
            0x1200cf,
            0xffa500,
            0xdaff00,
            0x5aff00,
            0x00ff25,
            0x00ffa5,
            0x00daff,
            0x005aff,
            0x2500ff,
            0xa500ff,
            0xff00d9,
            0xff005a,
            0xff2500,
            0x00b259,
            0x00b259
        ]
        SRC_COLORS = [self.hex_to_rgb(color) for color in SRC_COLORS]
        REPLACEMENT_COLORS = [self.hex_to_rgb(color) for color in REPLACEMENT_COLORS]
        if self.bird_id != -1:
            random.seed(self.bird_id)
        color_mapping = {SRC_COLORS[i]: random.choice(REPLACEMENT_COLORS) for i in range(len(SRC_COLORS))}
        while color_mapping[SRC_COLORS[1]] == self.hex_to_rgb(0x000000):
            # beak color should not be black
            color_mapping[SRC_COLORS[1]] = random.choice(REPLACEMENT_COLORS)
        for image in self.images.images:
            self.change_color(image, color_mapping)
        random.seed()

    def update(self):
        if self.kill_self:
            if random.randint(0, 8) == 0:
                self.jump()
        super().update()

    def turn_off_brain(self):
        self.kill_self = True

    @classmethod
    def kill_random(cls):
        defaultbird_instances = []
        for child in cls.child:
            if isinstance(child, DefaultBird) and not child.kill_self:
                defaultbird_instances.append(child)
        if not defaultbird_instances:
            return
        idx = random.randint(0, len(defaultbird_instances) - 1)
        defaultbird_instances[idx].turn_off_brain()

    @staticmethod
    def hex_to_rgb(hex: int) -> tuple[int, int, int]:
        r = (hex & 0xff0000) >> 16
        g = (hex & 0x00ff00) >> 8
        b = (hex & 0x0000ff)
        return r, g, b

    @staticmethod
    def change_color(surface: pygame.image, color_mapping: dict[tuple[int, int, int], tuple[int, int, int]]):
        width, height = surface.get_size()
        for x in range(width):
            for y in range(height):
                pixel_color = surface.get_at((x, y))
                transparent = pixel_color.a == 0
                pixel_color = (pixel_color.r, pixel_color.g, pixel_color.b)

                # check if pixel is transparent
                if transparent:
                    continue

                # Check if the pixel color needs to be replaced
                if pixel_color in color_mapping:
                    new_color = color_mapping[pixel_color]
                    surface.set_at((x, y), new_color)

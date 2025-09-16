import pygame


class Animated:
    def __init__(self, images: list[pygame.image], fps: int, time_per_frame: int = 1):
        self.images = images
        self.fps = fps
        self.time_per_frame = time_per_frame
        self.frame = 0
        self.frame_count = 0

    def get_frame(self) -> pygame.image:
        return self.images[self.frame]

    def update(self) -> None:
        self.frame_count += 1
        if self.frame_count % self.time_per_frame == 0:
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0

    def reset(self) -> None:
        self.frame = 0
        self.frame_count = 0

    def __str__(self):
        return f"Animated: {self.frame} {self.frame_count}"

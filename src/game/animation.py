import pygame

class Animation:
    def __init__(self, sprite_sheet: pygame.Surface, frame_width: int, frame_height: int, num_frames: int, frame_duration: float):
        self.frames = []
        for i in range(num_frames):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            self.frames.append(sprite_sheet.subsurface(rect))
        self.current = 0
        self.timer = 0.0
        self.frame_duration = frame_duration  # сек на кадр

    def update(self, dt: float, moving: bool):
        if moving:
            self.timer += dt
            if self.timer >= self.frame_duration:
                self.timer -= self.frame_duration
                self.current = (self.current + 1) % len(self.frames)
        else:
            # если не движется — кадр №0
            self.current = 0
            self.timer = 0.0

    def get_image(self) -> pygame.Surface:
        return self.frames[self.current]

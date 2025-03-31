import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=(255, 0, 0), width=5, height=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):

        self.rect.y -= self.speed


        if self.rect.bottom < 0:
            self.kill()
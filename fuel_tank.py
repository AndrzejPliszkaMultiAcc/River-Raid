import pygame

class FuelTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 30))
        self.image.fill((255, 255, 0))


        font = pygame.font.Font(None, 24)
        text = font.render("F", True, (0, 0, 0))
        text_rect = text.get_rect(center=(10, 15))
        self.image.blit(text, text_rect)

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 2
        if self.rect.top > 500:
            self.kill()

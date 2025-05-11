import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=(0, 0, 255), width=25, height=25):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()

        # Ruch w górę, jeśli nie jesteśmy przy górnej krawędzi
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        # Ruch w dół, jeśli nie jesteśmy przy dolnej krawędzi
        if keys[pygame.K_s] and self.rect.bottom < 500:  # 500 to wysokość okna
            self.rect.y += self.speed
        # Ruch w lewo, jeśli nie jesteśmy przy lewej krawędzi
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        # Ruch w prawo, jeśli nie jesteśmy przy prawej krawędzi
        if keys[pygame.K_d] and self.rect.right < 500:  # 500 to szerokość okna
            self.rect.x += self.speed

    def collect_fuel(self, fuel_tanks, hud):
        hits = pygame.sprite.spritecollide(self, fuel_tanks, dokill=True)
        for hit in hits:
            hud.add_energy(20)

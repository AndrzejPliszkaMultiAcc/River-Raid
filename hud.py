import pygame

class HUD:
    def __init__(self, surface):
        self.surface = surface
        self.energy = 100
        self.energy_timer = 0

    def update(self):
        self.energy_timer += 1
        if self.energy_timer >= 60:
            self.energy = max(0, self.energy - 5)
            self.energy_timer = 0

    def add_energy(self, amount):
        self.energy = min(100, self.energy + amount) #energia nie wyjdzie poza 100

    def draw(self):
        max_width = 100
        height = 10
        x = self.surface.get_width() - max_width - 10
        y = self.surface.get_height() - height - 10

        pygame.draw.rect(self.surface, (100, 100, 100), (x, y, max_width, height))
        energy_width = int((self.energy / 100) * max_width)
        pygame.draw.rect(self.surface, (0, 255, 0), (x, y, energy_width, height))
        pygame.draw.rect(self.surface, (255, 255, 255), (x, y, max_width, height), 1)

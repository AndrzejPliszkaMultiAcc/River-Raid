import pygame
import random


class FuelTank(pygame.sprite.Sprite):
    def __init__(self, x, y, game_map=None):
        super().__init__()
        self.image = pygame.Surface((20, 30))
        self.image.fill((255, 255, 0))

        font = pygame.font.Font(None, 24)
        text = font.render("F", True, (0, 0, 0))
        text_rect = text.get_rect(center=(10, 15))
        self.image.blit(text, text_rect)

        self.rect = self.image.get_rect(center=(x, y))
        self.map = game_map

    def update(self):
        self.rect.y += self.map.velocity
        if self.rect.top > self.map.screen_height:
            self.kill()

    @staticmethod #sprawdza kolizje, generuje 10 prób dobrego miejsca
    def spawn_valid(map_instance, max_tries=10):
        for _ in range(max_tries):
            x = random.randint(0, map_instance.screen_width - 20)
            y = -30
            tank_rect = pygame.Rect(x, y, 20, 30) #prostokąt do sprawdzania kolizji

            collision_ranges = map_instance.get_collisions(y, 30) #bierze z get collisions przedziały w których respi się tank

            collides = any( #sprawdza czy tank przecina się z częścią mapy
                not (tank_rect.right < start or tank_rect.left > end) #jeśli prawy bok tanku jest przed początkiem ściany
                for (start, end) in collision_ranges
            )

            if not collides:
                return FuelTank(x + 10, y + 15, map_instance)  #zwraca tank z poprawionym środkiem

        return None  #zwraca nic jak nie znaleziono dobrej pozycji

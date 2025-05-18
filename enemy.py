from ctypes import windll

import pygame
import random
#COPIED FROM FUEL TANK, consider making a parent class and refactor this
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, game_map=None):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.map = game_map

    def update(self):
        self.rect.y += self.map.velocity
        if self.rect.top > self.map.screen_height:
            self.kill()

    @staticmethod #sprawdza kolizje, generuje 10 prób dobrego miejsca
    def spawn_valid(map_instance, max_tries=10):
        height = 60
        width = 60
        for _ in range(max_tries):
            x = random.randint(0, map_instance.screen_width - width)
            y = -height
            enemy_rect = pygame.Rect(x, y, width, height) #prostokąt do sprawdzania kolizji

            collision_ranges = map_instance.get_collisions(y, height) #bierze z get collisions przedziały w których respi się tank

            collides = any( #sprawdza czy tank przecina się z częścią mapy
                not (enemy_rect.right < start or enemy_rect.left > end) #jeśli prawy bok tanku jest przed początkiem ściany
                for (start, end) in collision_ranges
            )

            if not collides:
                return Enemy(x + width/2, y + height/2, map_instance)  #zwraca tank z poprawionym środkiem

        return None  #zwraca nic jak nie znaleziono dobrej pozycji

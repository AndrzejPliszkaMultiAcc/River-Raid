import pygame
from map import Map


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=(0, 0, 255), width=25, height=25):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.game_map = None
        self.map_speed_changed = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Moving right unless player is at the edge
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        # Moving right unless the player is at the edge
        if keys[pygame.K_d] and self.rect.right < 500:  # 500 to szerokość okna
            self.rect.x += self.speed
        if self.game_map:
            if keys[pygame.K_w] and not self.map_speed_changed:
                self.game_map.velocity = min(24, self.game_map.base_velocity + 5)
                self.map_speed_changed = True
            elif keys[pygame.K_s] and not self.map_speed_changed:
                self.game_map.velocity = max(1, self.game_map.base_velocity - 5)
                self.map_speed_changed = True
            elif not keys[pygame.K_w] and not keys[pygame.K_s]:
                self.game_map.velocity = self.game_map.base_velocity
                self.map_speed_changed = False

        if self.game_map:
            collision_ranges = self.game_map.get_collisions(self.rect.top, self.rect.height)
            for (start_x, end_x) in collision_ranges:
                if not (self.rect.right < start_x or self.rect.left > end_x):
                    print("kolizja")
                    break

    def collect_fuel(self, fuel_tanks, hud):
        hits = pygame.sprite.spritecollide(self, fuel_tanks, dokill=True)
        for hit in hits:
            hud.add_energy(20)

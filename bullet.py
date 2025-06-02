import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10, color=(255, 0, 0), width=5, height=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):

        self.rect.y -= self.speed


        if self.rect.bottom < 0:
            self.kill()

    def check_if_hit_destroyable_object(self, destroyable_objects, increment_counter=None):
        hits = pygame.sprite.spritecollide(self, destroyable_objects, dokill=True)
        for hit in hits:
            hit.kill()
            self.kill()
            if increment_counter:
                increment_counter()

    def check_if_hit_wall(self, map):
        collisions = map.get_collisions(self.rect.y, self.rect.height)
        for collision in collisions:
            if collision[0] < self.rect.x < collision[1]:
                self.kill()
                break
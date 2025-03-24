import pygame
import map
import time

from map import TerrainStructures
from bullet import Bullet

pygame.init()
color = (255, 255, 255)
position = (0, 0)
canvas = pygame.display.set_mode((500, 500))

canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("River Raid")

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

running = True
map_object = map.Map(canvas)
while running:
    canvas.fill((0, 0, 0))
    map_object.move_blocks()
    map_object.display_saved_blocks()
    map_object.remove_redundant_blocks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(250, 450) #current plane position
                all_sprites.add(bullet)

    all_sprites.update()
    all_sprites.draw(canvas)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

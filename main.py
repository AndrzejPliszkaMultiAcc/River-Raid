import pygame
import map
import time

from map import TerrainStructures
import random
from bullet import Bullet
from fuel_tank import FuelTank
from player import Player

pygame.init()
color = (255, 255, 255)
position = (0, 0)
canvas = pygame.display.set_mode((500, 500))

canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("River Raid")

all_sprites = pygame.sprite.Group()
fuel_tanks = pygame.sprite.Group()
clock = pygame.time.Clock()

player = Player(250, 485)
all_sprites.add(player)

running = True
map_object = map.Map(canvas)
spawn_timer = 0
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
                bullet = Bullet(player.rect.centerx, player.rect.centery) #current plane position
                all_sprites.add(bullet)

    if spawn_timer <= 0:
        x = random.randint(50, 450)
        fuel_tank = FuelTank(x, -20)
        all_sprites.add(fuel_tank)
        fuel_tanks.add(fuel_tank)
        spawn_timer = random.randint(60, 180)
    else:
        spawn_timer -= 1

    all_sprites.update()
    all_sprites.draw(canvas)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
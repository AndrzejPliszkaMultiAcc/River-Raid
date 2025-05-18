import pygame
import map
import time

from map import TerrainStructures
import random
from bullet import Bullet
from fuel_tank import FuelTank
from enemy import Enemy
from player import Player
from hud import HUD

pygame.init()
color = (255, 255, 255)
position = (0, 0)
canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("River Raid")

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
fuel_tanks = pygame.sprite.Group()
enemies = pygame.sprite.Group()
clock = pygame.time.Clock()

player = Player(250, 485)
map_object = map.Map(canvas)
player.game_map = map_object
all_sprites.add(player)
hud = HUD(canvas)

fuel_tank_spawn_timer = 0
enemy_spawn_timer = 0
running = True

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
                bullets.add(bullet)
                all_sprites.add(bullet)

    if fuel_tank_spawn_timer <= 0:
        fuel_tank = FuelTank.spawn_valid(map_object)
        if fuel_tank:
            all_sprites.add(fuel_tank)
            fuel_tanks.add(fuel_tank)
        fuel_tank_spawn_timer = random.randint(60, 180)
    else:
        fuel_tank_spawn_timer -= 1

    #Possible code duplication, on adding more spawned objects consider refactoring
    if enemy_spawn_timer <= 0:
        enemy = Enemy.spawn_valid(map_object)
        if enemy:
            all_sprites.add(enemy)
            enemies.add(enemy)
        enemy_spawn_timer = random.randint(10, 60)
    else:
        enemy_spawn_timer -= 1

    hud.update()
    player.collect_fuel(fuel_tanks, hud)
    player.check_if_hit_by_enemy(enemies)
    for bullet in bullets:
        bullet.check_if_hit_destroyable_object(enemies)
        bullet.check_if_hit_destroyable_object(fuel_tanks)
        bullet.check_if_hit_wall(map_object)

    all_sprites.update()
    all_sprites.draw(canvas)
    hud.draw()

    pygame.display.update()
    clock.tick(60)
    #tymczasowe rozwiązanie na przegraną z powodu braku paliwa
    if hud.energy <= 0:
        running = False

pygame.quit()

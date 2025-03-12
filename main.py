import pygame
import map
import time

from map import TerrainStructures

pygame.init()
color = (255 ,255 ,255)
position = (0 ,0)

ticks_per_second = 30
canvas = pygame.display.set_mode((500 ,500))

pygame.display.set_caption("River Raid")

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

    pygame.display.update()
    time.sleep(1/ticks_per_second)

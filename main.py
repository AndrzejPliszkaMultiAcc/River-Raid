import pygame
import map
import time

pygame.init()
color = (255 ,255 ,255)
position = (0 ,0)

ticks_per_second = 30
canvas = pygame.display.set_mode((500 ,500))

pygame.display.set_caption("River Raid")

running = True
mapObject = map.Map(canvas)
while running:
    canvas.fill((0, 0, 0))
    mapObject.move_blocks()
    mapObject.display_saved_blocks()
    mapObject.remove_redundant_blocks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    time.sleep(1/ticks_per_second)

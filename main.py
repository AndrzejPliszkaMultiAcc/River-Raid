import pygame

pygame.init()
color = (255 ,255 ,255)
position = (0 ,0)

canvas = pygame.display.set_mode((500 ,500))

pygame.display.set_caption("River Raid")

running = True

while running:
    canvas.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

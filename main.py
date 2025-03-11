import pygame
from bullet import Bullet

pygame.init()
color = (255, 255, 255)
position = (0, 0)

canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("River Raid")

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

running = True
while running:
    canvas.fill((0, 0, 0))

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

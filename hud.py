import pygame
import time

class HUD:
    def __init__(self, surface):
        self.surface = surface
        self.energy = 100
        self.energy_timer = 0
        

        self.defeated_enemies = 0
        self.start_time = time.time()
        self.game_time = 0
        

        self.game_over = False

    def update(self):
        if not self.game_over:
            self.game_time = time.time() - self.start_time
            
        self.energy_timer += 1
        if self.energy_timer >= 60:
            self.energy = max(0, self.energy - 10)
            self.energy_timer = 0
            

        if self.energy <= 0:
            self.game_over = True

    def add_energy(self, amount):
        self.energy = min(100, self.energy + amount) #energia nie wyjdzie poza 100

    def draw(self):
        max_width = 100
        height = 10
        x = self.surface.get_width() - max_width - 10
        y = self.surface.get_height() - height - 10

        pygame.draw.rect(self.surface, (100, 100, 100), (x, y, max_width, height))
        energy_width = int((self.energy / 100) * max_width)
        pygame.draw.rect(self.surface, (0, 255, 0), (x, y, energy_width, height))
        pygame.draw.rect(self.surface, (255, 255, 255), (x, y, max_width, height), 1)
        
    def increment_defeated_enemies(self):
        self.defeated_enemies += 1
        
    def reset_stats(self):
        self.defeated_enemies = 0
        self.start_time = time.time()
        self.game_time = 0
        self.energy = 100
        self.energy_timer = 0
        self.game_over = False
        
    def show_game_over_screen(self):
        self.surface.fill((0, 0, 0))
        

        title_font = pygame.font.Font(None, 64)
        stats_font = pygame.font.Font(None, 32)
        info_font = pygame.font.Font(None, 24)
        

        title_text = title_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 - 70))
        self.surface.blit(title_text, title_rect)
        

        minutes = int(self.game_time // 60)
        seconds = int(self.game_time % 60)
        time_text = stats_font.render(f"Czas gry: {minutes}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 - 10))
        self.surface.blit(time_text, time_rect)
        
        enemies_text = stats_font.render(f"Pokonani wrogowie: {self.defeated_enemies}", True, (255, 255, 255))
        enemies_rect = enemies_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 + 30))
        self.surface.blit(enemies_text, enemies_rect)
        

        restart_text = info_font.render("Naciśnij 'P' aby rozpocząć nową grę", True, (200, 200, 0))
        restart_rect = restart_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 + 80))
        self.surface.blit(restart_text, restart_rect)
        
        pygame.display.update()

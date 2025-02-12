import pygame
class Map:
    def __init__(self, surface):
        self.surface = surface
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()
        self.block_list = [[0, 0], [2, 3], [2, 2]]
        self.y_offset = 0
        self.velocity = 10
        self.blocks_on_screen = 10
        self.block_width = self.screen_width / self.blocks_on_screen
        self.block_height = self.screen_height / self.blocks_on_screen

    def display_saved_blocks(self):
        for block in self.block_list:
            x_pos = block[0] * self.block_width
            y_pos = block[1] * self.block_height + self.y_offset
            pygame.draw.rect(self.surface, (0, 255, 0), [x_pos, y_pos, self.block_width, self.block_height])

    def move_blocks(self):
        if self.block_height < self.y_offset + self.velocity:
            for block in self.block_list:
                block[1] = block[1] + int((self.y_offset + self.velocity) / self.block_height)
            self.y_offset = (self.y_offset + self.velocity) % self.block_height
        else:
            self.y_offset = self.y_offset + self.velocity

    def remove_redundant_blocks(self):
        self.block_list = [x for x in self.block_list if x[1] <= 10]

    def spawn_line(self, line):
        pass
        #if (self.block_list)
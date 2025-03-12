from enum import Enum
import pygame

class MapTile:
    def __init__(self, height, width, expand_from_walls):
        self.height = height
        self.width = width
        self.fill_expand_from_walls = expand_from_walls

    def get_list_of_x_cords(self, block_width):
        list_of_x_cords = []
        if self.fill_expand_from_walls:
            for i in range(self.width):
                list_of_x_cords.append(i)
                list_of_x_cords.append(block_width-(1+i))
        else:
            for i in range(self.width, block_width-self.width):
                list_of_x_cords.append(i)
        return list_of_x_cords

class TerrainStructures(Enum):
    STRAIGHT_CORRIDOR = [
        MapTile(10, 5, True),
        MapTile(1, 4, True),
        MapTile(1, 3, True),
        MapTile(100, 2, True)
    ]

class Map:
    def __init__(self, surface):
        self.surface = surface
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()
        self.block_list = []
        self.y_offset = 0
        self.velocity = 10
        self.blocks_on_screen = 20
        self.block_width = self.screen_width / self.blocks_on_screen
        self.block_height = self.screen_height / self.blocks_on_screen
        self.next_line_to_spawn = []
        self.current_spawned_line = 0
        self.current_spawned_tile = 0
        self.current_spawned_structure = TerrainStructures.STRAIGHT_CORRIDOR

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
            self.spawn_line(self.next_line_to_spawn)
            self.update_next_line_to_spawn()
        else:
            self.y_offset = self.y_offset + self.velocity

    def remove_redundant_blocks(self):
        self.block_list = [x for x in self.block_list if x[1] <= self.blocks_on_screen]

    def spawn_line(self, list_of_x_cords):
        if any(point[1] <= -1 for point in self.block_list):
            return False
        else:
            for x_cord in list_of_x_cords:
                self.block_list.append([x_cord, -1])
            return True

    def update_next_line_to_spawn(self):
        map_tile_list = self.current_spawned_structure.value
        self.current_spawned_line += 1

        if self.current_spawned_tile >= len(map_tile_list):
            self.next_line_to_spawn = []
            return

        if self.current_spawned_line >= map_tile_list[self.current_spawned_tile].height:
            self.current_spawned_line = 0
            self.current_spawned_tile += 1

        if self.current_spawned_tile < len(map_tile_list):
            list_of_x_cords = map_tile_list[self.current_spawned_tile].get_list_of_x_cords(self.blocks_on_screen)
            self.next_line_to_spawn = list_of_x_cords

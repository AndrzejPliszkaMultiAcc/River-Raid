from enum import Enum
import pygame

# This class represents part of map in which all rows (in some height) are the same
class MapTile:
    def __init__(self, height, width, expand_from_walls, offset):
        self.height = height # Number of blocks the structure will occupy vertically
        self.width = width # Block to which the structure will be expanded
        self.fill_expand_from_walls = expand_from_walls # If False, structure will expand from center
        self.offset = offset # Number of blocks which will be added to the left and right side of the structure

    # Used to get list of x coordinates of blocks given parameters of tile (and number of horizontal blocks)
    def get_list_of_x_cords(self, block_width):
        list_of_x_cords = []
        if self.fill_expand_from_walls:
            for i in range(self.width):
                list_of_x_cords.append(i)
                list_of_x_cords.append(block_width-(1+i))
        else:
            for i in range(self.width, block_width-self.width):
                list_of_x_cords.append(i)
            for i in range(self.offset):
                list_of_x_cords.append(i)
                list_of_x_cords.append(block_width - (1 + i))

        return list_of_x_cords

# This class lists all structures of map
class TerrainStructures(Enum):
    MAP1 = [
        MapTile(20, 6, True, 0),
        MapTile(20, 5, True, 0),
        MapTile(20, 6, True, 0),
        MapTile(20, 5, True, 0),
        MapTile(20, 6, True, 0),
    ]
    STRAIGHT_CORRIDOR = [
        MapTile(10, 7, True, 0),
    ]
    MAP2 = [
        MapTile(6, 5, True, 0),
        MapTile(6, 4, True, 0),
        MapTile(2, 3, True, 0),
        MapTile(6, 4, True, 0),
        MapTile(6, 3, True, 0),
        MapTile(3, 2, True, 0),
        MapTile(14, 8, False, 2),
        MapTile(3, 3, True, 0),
        MapTile(7, 5, True, 0),
        MapTile(5, 3, True, 0),
        MapTile(6, 2, True, 0),
        MapTile(8, 8, False, 2),
        MapTile(3, 9, False, 2),
        MapTile(7, 2, True, 0),
        MapTile(6, 5, True, 0),
    ]
    MAP3 = [
        MapTile(10, 6, True, 0),
        MapTile(6, 4, True, 0),
        MapTile(8, 3, True, 0),
        MapTile(10, 5, True, 0),
        MapTile(9, 4, True, 0),
        MapTile(7, 3, True, 0),
        MapTile(5, 9, False, 4),
        MapTile(12, 8, False, 3),
        MapTile(6, 3, True, 0),
        MapTile(7, 6, True, 0),
        MapTile(4, 4, True, 0),
        MapTile(10, 8, False, 2),
        MapTile(9, 7, False, 2),
        MapTile(10, 4, True, 0),
        MapTile(10, 8, True, 0),
    ]

class Map:
    def __init__(self, surface):
        self.surface = surface # Canvas on which the map will be drawn
        self.screen_width = surface.get_width() # Screen width in pixels
        self.screen_height = surface.get_height() # Screen height in pixels
        self.block_list = [] # List of all blocks on the screen
        self.y_offset = 0 # Offset of blocks in relation to full block (always positive)
        self.base_velocity = 10  #
        self.velocity = self.base_velocity #max 24, min 1, INTENDED TO BE MODIFIED IN RUNTIME
        self.blocks_on_screen = 20 # Number of blocks on the screen
        self.block_width = self.screen_width / self.blocks_on_screen # Width of one block in pixels (read only)
        self.block_height = self.screen_height / self.blocks_on_screen # Height of one block in pixels (read only)
        self.next_line_to_spawn = [] # List of x coordinates of blocks which will be spawned next
        self.current_spawned_line = 0 # Current spawned line of map tile
        self.current_spawned_tile = 0 # Current spawned tile of structure
        self.map_structures = [TerrainStructures.STRAIGHT_CORRIDOR, TerrainStructures.MAP1, TerrainStructures.STRAIGHT_CORRIDOR, TerrainStructures.MAP2,  TerrainStructures.STRAIGHT_CORRIDOR, TerrainStructures.MAP3] # List of structures displayed in order (creates map)
        self.current_spawned_structure_index = 0
        self.current_spawned_structure = self.map_structures[self.current_spawned_structure_index]

        # <-- ZMIANA: wczytanie i przeskalowanie obrazka bloku
        self.block_image = pygame.image.load("ic9.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (int(self.block_width), int(self.block_height)))

    # <-- ZMIANA: wyświetlanie obrazków zamiast zielonych prostokątów
    def display_saved_blocks(self):
        for block in self.block_list:
            x_pos = block[0] * self.block_width
            y_pos = block[1] * self.block_height + self.y_offset
            self.surface.blit(self.block_image, (x_pos, y_pos))  # <-- ZMIANA

    # Moves blocks down the screen according to velocity
    def move_blocks(self):
        if self.block_height < self.y_offset + self.velocity:
            for block in self.block_list:
                block[1] = block[1] + int((self.y_offset + self.velocity) / self.block_height)
            self.y_offset = (self.y_offset + self.velocity) % self.block_height
            self.spawn_line(self.next_line_to_spawn)
            self.update_next_line_to_spawn()
        else:
            self.y_offset = self.y_offset + self.velocity

    # Removes blocks which are not on the screen
    def remove_redundant_blocks(self):
        self.block_list = [x for x in self.block_list if x[1] <= self.blocks_on_screen]

    # Spawns set line of blocks on the screen
    def spawn_line(self, list_of_x_cords):
        if any(point[1] <= -1 for point in self.block_list):
            return False
        else:
            for x_cord in list_of_x_cords:
                self.block_list.append([x_cord, -1])
            return True

    # Logic related to choosing what to spawn next
    def update_next_line_to_spawn(self):
        map_tile_list = self.current_spawned_structure.value

        if self.current_spawned_line >= map_tile_list[self.current_spawned_tile].height:
            self.current_spawned_line = 0
            self.current_spawned_tile += 1

        if self.current_spawned_tile >= len(map_tile_list):
            self.current_spawned_structure_index += 1
            if self.current_spawned_structure_index >= len(self.map_structures):
                self.current_spawned_structure_index = 0
            self.current_spawned_structure = self.map_structures[self.current_spawned_structure_index]
            self.current_spawned_line = 0
            self.current_spawned_tile = 0

        if self.current_spawned_tile < len(map_tile_list):
            list_of_x_cords = map_tile_list[self.current_spawned_tile].get_list_of_x_cords(self.blocks_on_screen)
            self.next_line_to_spawn = list_of_x_cords

        self.current_spawned_line += 1

    # USE THIS FOR COLLISION!
    # Params: y_pixel_pos - y position in pixels, always give most upper point!
    #         height_pixels - height of area to check in pixels
    #         draw_debug - if True, draws area of checking and blocks, use if you think function is malfunctioning
    # Returns list of tuples with ranges where are blocks (so if x coordinate is in range, there should be collision)
    def get_collisions(self, y_pos, height, draw_debug=False):
        y_start = y_pos
        y_end = y_pos + height

        # Bloki mogą się kończyć w połowie przedziału, więc musimy dokładnie sprawdzić każdy
        wall_blocks = []

        for block in self.block_list:
            block_y_start = block[1] * self.block_height + self.y_offset
            block_y_end = block_y_start + self.block_height

            # Sprawdź czy przedział gracza nachodzi na blok w pionie
            if block_y_end >= y_start and block_y_start <= y_end:
                wall_blocks.append(block)

        # Zbieramy wszystkie x w pikselach
        x_pixels = [block[0] * self.block_width for block in wall_blocks]
        x_pixels.sort()

        # Tworzenie przedziałów ciągłych
        x_ranges = []
        if x_pixels:
            range_start = x_pixels[0]
            last_x = x_pixels[0]

            for x in x_pixels[1:]:
                if x <= last_x + self.block_width:
                    last_x = x
                else:
                    x_ranges.append((range_start, last_x + self.block_width))
                    range_start = x
                    last_x = x

            x_ranges.append((range_start, last_x + self.block_width))

        # Debug — obszar sprawdzania
        if draw_debug:
            pygame.draw.rect(self.surface, (255, 0, 0),
                             pygame.Rect(0, y_start, self.screen_width, height), 1)

            for x_start, x_end in x_ranges:
                pygame.draw.rect(
                    self.surface, (0, 255, 255),
                    pygame.Rect(x_start, y_start, x_end - x_start, height), 1)

        return x_ranges
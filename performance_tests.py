import time
import platform
import psutil
import pygame
import multiprocessing
from map import Map
from fuel_tank import FuelTank
from enemy import Enemy


pygame.init()
screen = pygame.display.set_mode((500, 500))
game_map = Map(screen)

def print_system_info():
    print("=== SYSTEM INFORMATION ===")
    print(f"Platform        : {platform.system()} {platform.release()}")
    print(f"CPU cores       : {multiprocessing.cpu_count()}")
    print(f"CPU             : {platform.processor()}")
    print(f"Total RAM       : {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
    print(f"Python version  : {platform.python_version()}")
    print(f"Pygame version  : {pygame.version.ver}")


def fill_map_blocks(n=1000):
    game_map.block_list = [[i % 10, i // 10] for i in range(n)]

def timeit(func, *args, n=100):
    start = time.perf_counter()
    for _ in range(n):
        func(*args)
    end = time.perf_counter()
    avg_time = (end - start) / n
    print(f"{func.__name__:<35}: {avg_time:.6f} s (avg over {n} runs)")

def test_update_next_line():
    timeit(game_map.update_next_line_to_spawn)

def test_move_blocks():
    fill_map_blocks()
    timeit(game_map.move_blocks)

def test_get_collisions():
    fill_map_blocks()
    y_pixel = 100
    height_pixels = 30
    timeit(game_map.get_collisions, y_pixel, height_pixels)

def test_display_saved_blocks():
    fill_map_blocks()
    timeit(game_map.display_saved_blocks)

def test_spawn_valid_fuel():
    fill_map_blocks()
    timeit(FuelTank.spawn_valid, game_map)

def test_spawn_valid_enemy():
    fill_map_blocks()
    timeit(Enemy.spawn_valid, game_map)

def run_all_tests():
    print_system_info()
    print("=== PERFORMANCE TESTS ===")
    test_update_next_line()
    test_move_blocks()
    test_get_collisions()
    test_display_saved_blocks()
    test_spawn_valid_fuel()
    test_spawn_valid_enemy()

if __name__ == "__main__":
    run_all_tests()

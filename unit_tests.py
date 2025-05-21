
import unittest
import pygame
from player import Player
from bullet import Bullet
from enum import Enum
from unittest import mock
from map import MapTile, Map


class TestMapTile(unittest.TestCase):
    def test_get_list_of_x_cords_expanding(self):
        tile = MapTile(height=1, width=2, expand_from_walls=True, offset=0)
        result = tile.get_list_of_x_cords(10)
        self.assertEqual(result, [0, 9, 1, 8])

    def test_get_list_of_x_cords_non_expanding(self):
        tile = MapTile(height=1, width=2, expand_from_walls=False, offset=1)
        result = tile.get_list_of_x_cords(10)
        self.assertEqual(result, [2, 3, 4, 5, 6, 7, 0, 9])


class TestMapFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.surface = pygame.Surface((800, 600))
        self.map_instance = Map(self.surface)

    def test_get_list_of_x_cords(self):
        tile = MapTile(height=1, width=3, expand_from_walls=True, offset=0)
        result = tile.get_list_of_x_cords(10)
        expected = [0, 9, 1, 8, 2, 7]  # Zakładając, że expand_from_walls działa poprawnie
        self.assertEqual(result, expected)

    def test_display_saved_blocks(self):
        self.map_instance.block_list = [[1, 2], [3, 4]]
        self.map_instance.display_saved_blocks()  # Powinno działać bez błędów

    def test_move_blocks(self):
        self.map_instance.block_list = [[5, 5], [6, 6]]
        self.map_instance.y_offset = 0
        self.map_instance.velocity = 5
        self.map_instance.move_blocks()
        self.assertTrue(all(block[1] >= 5 for block in self.map_instance.block_list))

    def test_remove_redundant_blocks(self):
        self.map_instance.block_list = [[2, 10], [3, 21], [4, 5]]
        self.map_instance.blocks_on_screen = 20
        self.map_instance.remove_redundant_blocks()
        self.assertNotIn([3, 21], self.map_instance.block_list)

    def test_spawn_line(self):
        result = self.map_instance.spawn_line([2, 4, 6])
        self.assertTrue(result)
        self.assertIn([2, -1], self.map_instance.block_list)
        self.assertIn([4, -1], self.map_instance.block_list)
        self.assertIn([6, -1], self.map_instance.block_list)

    def test_update_next_line_to_spawn(self):
        self.map_instance.update_next_line_to_spawn()
        self.assertTrue(len(self.map_instance.next_line_to_spawn) > 0)

    def test_get_collisions_basic(self):
        fake_surface = pygame.Surface((800, 600))
        test_map = Map(fake_surface)

        test_map.block_width = 40
        test_map.block_height = 40
        test_map.y_offset = 0

        test_map.block_list = [[2, 3],[3, 3],[5, 4], [6, 5],[7, 5]]

        y_pos = 115
        height = 90
        x_ranges = test_map.get_collisions(y_pos, height)
        expected = [(80, 160), (200, 320)]
        assert x_ranges == expected

    def test_get_collisions_advanced(self):
        fake_surface = pygame.Surface((800, 600))
        test_map = Map(fake_surface)

        test_map.block_width = 40
        test_map.block_height = 40
        test_map.y_offset = 0

        test_map.block_list = [
            [1, 2], [2, 2], [3, 2]
        ]

        y_pos = 80
        height = 40
        x_ranges = test_map.get_collisions(y_pos, height)

        expected = [(40, 160)]
        assert x_ranges == expected

    def test_get_collisions_gaps(self):
        fake_surface = pygame.Surface((800, 600))
        test_map = Map(fake_surface)

        test_map.block_width = 40
        test_map.block_height = 40
        test_map.y_offset = 0

        test_map.block_list = [[1, 3], [3, 3], [6, 3]]

        y_pos = 120
        height = 40
        x_ranges = test_map.get_collisions(y_pos, height)

        expected = [(40, 80), (120, 160), (240, 280)]  # oddzielne bloki
        assert x_ranges == expected


class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.surface = pygame.Surface((500, 500))
        self.map_instance = Map(self.surface)
        self.player = Player(250, 485)
        self.player.game_map = self.map_instance

    def test_initial_position(self):
        self.assertEqual(self.player.rect.centerx, 250)
        self.assertEqual(self.player.rect.centery, 485)

    def test_player_does_not_move_beyond_left_boundary(self):
        self.player.rect.left = 0
        keys = [False] * 512
        keys[pygame.K_a] = True

        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            self.player.update()
            self.assertEqual(self.player.rect.left, 0)

    def test_player_moves_right(self):
        old_x = self.player.rect.x
        keys = [False] * 512
        keys[pygame.K_d] = True

        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            self.player.update()
            self.assertGreater(self.player.rect.x, old_x)

class DummyDestroyable(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class DummyMap:
    def __init__(self, collision_ranges):
        self.collision_ranges = collision_ranges

    def get_collisions(self, y, height):
        return self.collision_ranges

class TestBullet(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))
        self.bullet = Bullet(x=100, y=100)

    def test_check_if_hit_destroyable_object_hit(self):
        destroyable = DummyDestroyable(95, 95)  # Overlaps bullet
        group = pygame.sprite.Group(destroyable)

        all_sprites = pygame.sprite.Group(self.bullet)
        self.assertIn(self.bullet, all_sprites)

        self.bullet.check_if_hit_destroyable_object(group)

        self.assertNotIn(destroyable, group)
        self.assertFalse(self.bullet.alive())  # bullet should be killed

    def test_check_if_hit_destroyable_object_no_hit(self):
        destroyable = DummyDestroyable(200, 200)  # Far from bullet
        group = pygame.sprite.Group(destroyable)

        bullet_group = pygame.sprite.Group(self.bullet)  # Dodaj bullet do grupy
        self.bullet.check_if_hit_destroyable_object(group)

        self.assertIn(destroyable, group)
        self.assertTrue(self.bullet.alive())  # Teraz będzie True, bo bullet jest w grupie

    def test_check_if_hit_wall_hit(self):
        # Bullet.x = 100, range includes 90-110 => hit
        game_map = DummyMap(collision_ranges=[(90, 110)])
        all_sprites = pygame.sprite.Group(self.bullet)

        self.bullet.check_if_hit_wall(game_map)

        self.assertFalse(self.bullet.alive())

    def test_check_if_hit_wall_no_hit(self):
        game_map = DummyMap(collision_ranges=[(0, 80), (120, 140)])
        bullet_group = pygame.sprite.Group(self.bullet)  # Dodaj bullet do grupy
        self.bullet.check_if_hit_wall(game_map)
        self.assertTrue(self.bullet.alive())

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()

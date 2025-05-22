
import unittest
import pygame
from player import Player
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

    def test_increase_map_speed_with_w_key(self):
        self.map_instance.base_velocity = 10
        self.map_instance.velocity = 10
        keys = [False] * 512
        keys[pygame.K_w] = True

        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            self.player.update()
            self.assertEqual(self.map_instance.velocity, 15)
            self.assertTrue(self.player.map_speed_changed)

    def test_decrease_map_speed_with_s_key(self):
        self.map_instance.base_velocity = 10
        self.map_instance.velocity = 10
        keys = [False] * 512
        keys[pygame.K_s] = True

        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            self.player.update()
            self.assertEqual(self.map_instance.velocity, 5)
            self.assertTrue(self.player.map_speed_changed)

    def test_reset_map_speed_when_no_keys_pressed(self):
        self.player.map_speed_changed = True
        self.map_instance.base_velocity = 10
        self.map_instance.velocity = 20
        keys = [False] * 512

        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            self.player.update()
            self.assertEqual(self.map_instance.velocity, 10)
            self.assertFalse(self.player.map_speed_changed)

    def test_collision_detection_triggers_print(self):
        self.map_instance.get_collisions = unittest.mock.MagicMock(return_value=[(200, 300)])
        self.player.rect.left = 250
        self.player.rect.right = 260
        keys = [False] * 512

        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys), \
             unittest.mock.patch('builtins.print') as mocked_print:
            self.player.update()
            mocked_print.assert_called_with("kolizja")

    def test_collect_fuel_adds_energy(self):
        fuel_tank = pygame.sprite.Sprite()
        fuel_tank.rect = self.player.rect.copy()
        fuel_group = pygame.sprite.Group(fuel_tank)

        hud_mock = unittest.mock.MagicMock()
        self.player.collect_fuel(fuel_group, hud_mock)

        hud_mock.add_energy.assert_called_with(20)
        self.assertEqual(len(fuel_group), 0)

    def test_check_if_hit_by_enemy_triggers_quit(self):
        enemy = pygame.sprite.Sprite()
        enemy.rect = self.player.rect.copy()
        enemy_group = pygame.sprite.Group(enemy)

        with unittest.mock.patch('pygame.quit') as mock_quit:
            self.player.check_if_hit_by_enemy(enemy_group)
            mock_quit.assert_called_once()



if __name__ == '__main__':
    unittest.main()

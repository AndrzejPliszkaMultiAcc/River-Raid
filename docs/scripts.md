# scripts.md

## Table of Contents
1. [Unit Tests](#unit-tests)
    - MapTile
    - Map
    - Player
    - Bullet
    - FuelTank
    - HUD
2. [Performance Tests](#performance-tests)
    - System Info
    - Tested Map Functions
3. [Class and Method Descriptions](#class-and-method-descriptions)
    - MapTile
    - Map
    - Player
    - Bullet
    - FuelTank
    - HUD

---

## Unit Tests

### TestMapTile
- `test_get_list_of_x_cords_expanding` – verifies correct expansion of X coordinates when `expand_from_walls=True`
- `test_get_list_of_x_cords_non_expanding` – tests without expansion, including offset

### TestMapFunctions
- `test_get_list_of_x_cords` – general verification of returned coordinates
- `test_display_saved_blocks` – triggers block rendering
- `test_move_blocks` – verifies block movement
- `test_remove_redundant_blocks` – removes blocks outside the screen
- `test_spawn_line` – checks correct creation of a line of blocks
- `test_update_next_line_to_spawn` – tests updating spawn data
- `test_get_collisions_*` – a series of collision tests for different scenarios

### TestPlayer
- `test_initial_position` – verifies player's initial position
- `test_player_does_not_move_beyond_left_boundary` – limits leftward movement
- `test_player_moves_right` – tests movement to the right
- `test_increase_map_speed_with_w_key` – increases map speed with W key
- `test_decrease_map_speed_with_s_key` – decreases map speed with S key
- `test_reset_map_speed_when_no_keys_pressed` – resets map speed when no keys are pressed
- `test_collision_detection_triggers_print` – collision triggers a print message
- `test_collect_fuel_adds_energy` – tests fuel collection adding energy
- `test_check_if_hit_by_enemy_triggers_quit` – enemy collision triggers game quit

### TestBullet
- `test_bullet_initialization` – initializes position and velocity
- `test_bullet_update_movement` – tests bullet movement
- `test_bullet_kill_when_out_of_screen` – kills bullet after leaving the screen
- `test_bullet_hit_destroyable_object` – collision with destroyable objects
- `test_bullet_hit_wall` – collision with walls

### TestFuelTank
- `test_fuel_tank_initialization` – initializes fuel tank
- `test_fuel_tank_update_movement` – movement adjusted for map speed
- `test_fuel_tank_kill_when_out_of_screen` – removes tank after leaving screen
- `test_spawn_valid_returns_none_on_collision` – tests spawn failure due to collision

### TestHUD
- `test_hud_initialization` – correct initialization
- `test_update_decreases_energy` – energy decreases over time
- `test_add_energy_with_limit` – limits energy to 100 units
- `test_add_energy_normal` – normal energy addition

---

## Performance Tests

This script contains functions to test performance of map operations.

### System Info
Output by `print_system_info()`:
- platform
- processor
- number of cores
- RAM amount
- Python and Pygame version

### Tested Functions:

- `update_next_line_to_spawn()`
- `move_blocks()`
- `get_collisions(y_pixel, height_pixels)`
- `display_saved_blocks()`
- `FuelTank.spawn_valid(map)`
- `Enemy.spawn_valid(map)`

Each function is measured `n=100` times and the average execution time is printed.

---

## Class and Method Descriptions

### MapTile
- `get_list_of_x_cords(width)` – generates a list of X coordinates based on `expand_from_walls` flag and `offset`

### Map
- `spawn_line(x_cords)` – spawns a line of blocks based on X coordinates
- `update_next_line_to_spawn()` – updates data for the next spawn line
- `move_blocks()` – moves blocks according to `velocity`
- `remove_redundant_blocks()` – removes blocks outside the screen area
- `display_saved_blocks()` – draws blocks on screen
- `get_collisions(y, height)` – returns collision ranges

### Player
- `update()` – moves player, adjusts map speed, detects collisions
- `collect_fuel(fuel_group, hud)` – checks collisions with fuel
- `check_if_hit_by_enemy(enemy_group)` – checks collisions with enemies

### Bullet
- `update()` – moves bullet upward and kills it after leaving screen
- `check_if_hit_destroyable_object(group)` – destroys hit objects
- `check_if_hit_wall(map)` – detects collision with walls

### FuelTank
- `update()` – moves according to map velocity
- `spawn_valid(map)` – creates an object if no collision is detected

### HUD
- `update()` – decreases energy over time
- `add_energy(amount)` – adds energy with a maximum limit

---

## Notes
- All tests run in the `unittest` framework and are automated.
- Performance tests are not unit tests but are tools for measuring execution time.

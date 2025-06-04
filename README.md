# River-raid Project

This repository contains the core game scripts along with comprehensive unit and performance tests. The project is structured to ensure code reliability and efficiency.

---

## Overview

The project consists of:

- **Game logic scripts** managing the map, player, bullets, fuel tanks, HUD, and more.
- **Unit tests** verifying the correctness of each component.
- **Performance tests** measuring execution time of critical map operations.


## Getting Started

### Prerequisites

- Python 3.7+
- Pygame library

Install dependencies using:

```bash
pip install pygame
```
### Running the game
```bash
python main.py
```
### Running unit tests
Use unittest module:
```bash
python -m unittest discover tests/unit
```

---

## Project Structure
```bash
River-Raid [RiverRaid]
├── .venv
├── docs
│   └── scripts.md
├── sound
│   ├── explosion_sound.mp3
│   ...
├── bullet.py
├── enemy.py
├── fuel_tank.py
├── hud.py
├── main.py
├── map.py
├── performance_tests.py
├── player.py
├── README.md
├── requirements.txt
└── unit_tests.py
```

---

## More Information
Open docs/scripts.md for info what individual files and functions do.

## Our Team
- Olivier Pisarczyk (Leader)
- Olivier Malinowski
- Adam Pluta

# Space Invaders

## Overview
This is a custom implementation of the classic **Space Invaders** game built using the **Pygame** library. The game features dynamic texture changes for the player, aliens, and boss entities, background music, and sound effects. Players control a spaceship, shooting down waves of aliens and eventually facing a boss.

## Features
- **Random Textures**: The player, aliens, and boss have textures chosen randomly at the start of each game session.
- **Background Music and Sounds**: Dynamic background music and sound effects, including shooting, explosion, and alien kill sounds.
- **Player Controls**: Use arrow keys (or `A` and `D`) to move the player left and right. Press `SPACE` to shoot.
- **Levels and Progression**: Each level alternates between waves of aliens and a boss fight. The game becomes progressively harder with each level.
- **Game States**: Includes a menu, instructions screen, in-game mechanics, and a game-over screen.

## Controls
- `LEFT/RIGHT Arrow` or `A/D`: Move player spaceship left or right.
- `SPACE`: Shoot projectiles at aliens or the boss.
- The game features an automatic progression through levels, and a game-over state when lives are depleted.

## Classes and Structure

### 1. `Player`
- Represents the player-controlled spaceship.
- Attributes:
  - `image`: The texture used for the player, chosen randomly.
  - `rect`: The player's position and size.
  - `speed`: Movement speed of the player.
  - `lives`: Number of lives the player has.
  - `cooldown`: Time interval between shots.
- Key Methods:
  - `update()`: Handles player movement based on keyboard input.
  - `shoot()`: Fires a projectile if the cooldown period has passed.
  - `lose_life()`: Reduces player life count upon being hit by alien projectiles.
  - `gain_life()`: Increases player life count (e.g., when completing a level without losing a life).

### 2. `Alien`
- Represents an alien enemy.
- Attributes:
  - `image`: Randomly chosen texture for each alien.
  - `rect`: Position and size of the alien.
  - `direction`: Movement direction (left or right).
  - `speed`: Speed of the alien's movement.
- Key Methods:
  - `update()`: Moves the alien and changes direction upon hitting the screen edge.
  - `shoot()`: Fires a projectile.

### 3. `Boss`
- Represents a boss enemy that appears after every other level.
- Attributes:
  - `image`: Random texture for the boss.
  - `rect`: Position and size of the boss.
  - `health`: The boss's health points.
  - `speed`: Movement speed.
  - `shoot_interval`: Time interval between the boss’s projectile attacks.
- Key Methods:
  - `update()`: Handles boss movement and shooting mechanics.
  - `shoot()`: Fires three projectiles at different angles.

### 4. `Projectile`
- Represents a projectile fired by the player or an alien.
- Attributes:
  - `speed`: Speed of the projectile.
  - `angle`: The angle at which the projectile is fired (used by the boss for angled shots).
- Key Methods:
  - `update()`: Updates the projectile’s position based on its velocity.

## Main Functions

### `load_image()`
- Loads images (textures) dynamically with error handling.

### `load_sound()`
- Loads sound files for the game with error handling.

### `play_sound()`
- Plays a specific sound and pauses/unpauses background music.

### `spawn_aliens()`
- Spawns waves of alien enemies at the start of a level.

### `handle_level_progression()`
- Handles the progression between levels, spawning either a boss or alien wave.

### `handle_collisions()`
- Checks for collisions between player projectiles, aliens, alien projectiles, and the player.

### `handle_alien_shooting()`
- Manages when aliens fire projectiles.

### `display_score_and_lives()`
- Displays the player’s current score and lives on the screen.

## Game States
The game operates in different states:
- **MENU**: The starting screen with a "PLAY" button.
- **INSTRUCTIONS**: Provides the player with game instructions.
- **GAME**: The main gameplay state, which includes levels and shooting mechanics.
- **GAME_OVER**: Displayed when the player runs out of lives.

## Installation
1. Ensure you have Python installed.
2. Install the **Pygame** library using pip:
   ```bash
   pip install pygame
   ```
3. Clone this repository and navigate to the game directory:
   ```bash
    git clone https://github.com/nerkyzas157/Space_Invaders
    cd space-invaders   
    ```
4. Run the game:
   ```bash
   python main.py
   ```

## Assets
- Textures for the player, aliens, and boss are located in the textures/ directory.
- Background music and sound effects are located in the sounds/ directory.

## Contributing
Feel free to fork the repository and submit pull requests for any bug fixes or enhancements.

## License
This project is licensed under the MIT License.
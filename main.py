import pygame
import sys
import random
from pygame.locals import *
import math


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
NEON_GREEN = (57, 255, 20)
HIGHLIGHT_COLOR = (255, 215, 0)

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 40, bold=True)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")


# Load images and sounds dynamically with error handling
def load_image(path, colorkey=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if colorkey is not None:
            image.set_colorkey(colorkey)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        sys.exit()


def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Unable to load sound at {path}: {e}")
        sys.exit()


# Load Backgrounds
menu_bg = load_image("textures/bg/menu_bg.jpg")
normal_bg = load_image("textures/bg/normal_bg.jpg")
boss_bg = load_image("textures/bg/boss_bg.jpg")


# Load Textures with random selection
def get_random_texture(entity_type):
    return load_image(f"textures/{entity_type}/{random.randint(1,6)}.png")


player_image = get_random_texture("player")
alien_image = get_random_texture("aliens")
boss_image = get_random_texture("boss")

# Load Sounds
pygame.mixer.music.load("sounds/background/spaceinvaders.mpeg")
shoot_sound = load_sound("sounds/actions/shoot.wav")
explosion_sound = load_sound("sounds/actions/explosion.wav")
kill_sound = load_sound("sounds/actions/invaderkilled.wav")

# Start background music
pygame.mixer.music.play(-1)


# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(
            midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        )
        self.speed = 7
        self.lives = 3
        self.cooldown = 500  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self, keys):
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed

        # Constrain within screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            projectile = Projectile(self.rect.centerx, self.rect.top, -10)
            player_projectiles.add(projectile)
            self.last_shot = now
            play_sound(shoot_sound)

    def lose_life(self):
        self.lives -= 1
        play_sound(explosion_sound)
        if self.lives <= 0:
            self.kill()
            trigger_game_over()

    def gain_life(self):
        self.lives += 1


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = alien_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1  # 1 for right, -1 for left
        self.speed = speed

    def update(self):
        self.rect.x += self.speed * self.direction
        # Change direction and move down when hitting screen edges
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 5  # Move down
            # Might want to disable aliens going down if trying to reach ultimate high score.

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.bottom, 5)
        alien_projectiles.add(projectile)
        # play_sound(shoot_sound)
        # Disabled alien shooting sound due to performance issues.


class Boss(pygame.sprite.Sprite):
    def __init__(self, speed, health):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH // 2, 50))
        self.health = health
        self.speed = speed
        self.direction = 1
        self.last_shot = pygame.time.get_ticks()
        self.shoot_interval = 1000  # milliseconds

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1

        # Shooting logic
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_interval:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        # Shoot three projectiles: straight, left-angled, and right-angled
        middle_projectile = Projectile(
            self.rect.centerx, self.rect.bottom, 5, angle=0
        )  # Straight
        left_projectile = Projectile(
            self.rect.centerx, self.rect.bottom, 5, angle=-20
        )  # 20 degrees to the left
        right_projectile = Projectile(
            self.rect.centerx, self.rect.bottom, 5, angle=20
        )  # 20 degrees to the right

        alien_projectiles.add(middle_projectile, left_projectile, right_projectile)
        play_sound(shoot_sound)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle=0):
        super().__init__()
        self.image = pygame.Surface((8, 20))
        self.image.fill(NEON_GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.angle = math.radians(angle)  # Convert angle to radians for calculation
        self.velocity_x = speed * math.sin(self.angle)
        self.velocity_y = speed * math.cos(self.angle)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        # Remove projectile if it goes off-screen
        if (
            self.rect.bottom < 0
            or self.rect.top > SCREEN_HEIGHT
            or self.rect.right < 0
            or self.rect.left > SCREEN_WIDTH
        ):
            self.kill()


# Sound manager
def play_sound(sound):
    pygame.mixer.music.pause()
    sound.play()
    pygame.mixer.music.unpause()


# Game Over Trigger
def trigger_game_over():
    global game_state
    game_state = "GAME_OVER"


# Reset Game Function
def reset_game():
    global score, level, alien_speed, alien_shoot_interval, boss_speed, boss_health, no_life_lost, player, player_group
    score = 0
    level = 1
    alien_speed = 2
    alien_shoot_interval = 1000
    boss_speed = 2
    boss_health = 2
    no_life_lost = True
    # Reset player
    player = Player()
    player.image = get_random_texture("player")
    player_group = pygame.sprite.Group(player)
    player_projectiles.empty()
    alien_projectiles.empty()
    aliens.empty()
    boss_group.empty()


# Display Functions
def display_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)


def display_menu():
    screen.blit(menu_bg, (0, 0))
    # Define PLAY button rectangle
    play_button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100
    )
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Check if mouse is over PLAY button
    if play_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, play_button_rect)
        if mouse_pressed[0]:
            return "INSTRUCTIONS"
    else:
        pygame.draw.rect(screen, WHITE, play_button_rect, 2)  # Draw border

    display_text("PLAY", FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    return "MENU"


def display_instructions():
    screen.blit(normal_bg, (0, 0))
    # Instructions text
    instructions = [
        "Instructions:",
        "Use A/LEFT arrow to move left.",
        "Use D/RIGHT arrow to move right.",
        "Press SPACE to shoot.",
        "Destroy all aliens to advance.",
        "Defeat the boss to complete the level.",
        "Complete the level without losing a life and you'll get an additional life.",
        "Don't let aliens or their projectiles hit you!",
    ]

    for idx, line in enumerate(instructions):
        display_text(
            line,
            pygame.font.SysFont("Arial", 30),
            NEON_GREEN,
            screen,
            SCREEN_WIDTH // 2,
            150 + idx * 40,
        )

    # OK Button
    ok_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 150, 150, 50)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if ok_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, ok_button_rect)
        if mouse_pressed[0]:
            return "GAME"
    else:
        pygame.draw.rect(screen, WHITE, ok_button_rect, 2)

    display_text("OK", FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 125)
    return "INSTRUCTIONS"


def display_game_over():
    screen.blit(menu_bg, (0, 0))
    display_text(
        "GAME OVER",
        pygame.font.SysFont("Arial", 80, bold=True),
        RED,
        screen,
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 - 100,
    )
    display_text(
        f"Score: {score}", FONT, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    )

    # Retry Button
    retry_button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 80
    )
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if retry_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, retry_button_rect)
        if mouse_pressed[0]:
            reset_game()
            return "MENU"
    else:
        pygame.draw.rect(screen, WHITE, retry_button_rect, 2)

    display_text(
        "RETRY", FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90
    )
    pygame.event.clear()
    return "GAME_OVER"


# Initialize Sprite Groups
player = Player()
player_group = pygame.sprite.Group(player)
aliens = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()
alien_projectiles = pygame.sprite.Group()

# Game Variables
score = 0
level = 1
alien_speed = 2
alien_shoot_interval = 1000  # milliseconds
boss_speed = 2
boss_health = 2
last_alien_shot = pygame.time.get_ticks()
no_life_lost = True  # Track if the player loses a life during the level
game_state = "MENU"  # Possible states: MENU, INSTRUCTIONS, GAME, GAME_OVER


# Function to spawn aliens
def spawn_aliens():
    aliens.empty()
    for row in range(3):
        for col in range(8):
            x = 150 + col * 80
            y = 80 + row * 60
            alien = Alien(x, y, alien_speed)
            aliens.add(alien)


# Function to handle level progression
def handle_level_progression():
    global level, alien_speed, alien_shoot_interval, boss_speed, boss_health, no_life_lost, alien_image, boss_image

    if not aliens and not boss_group:
        if level % 2 == 0:
            # Spawn Boss
            boss = Boss(boss_speed, boss_health)
            boss_group.add(boss)
        else:
            # Spawn Aliens
            spawn_aliens()
        # Increase difficulty
        level += 1
        alien_speed *= 1.05
        alien_shoot_interval = max(200, int(alien_shoot_interval * 0.9))
        boss_speed *= 1.05
        boss_health += 1
        no_life_lost = True
        alien_image = get_random_texture("aliens")
        boss_image = get_random_texture("boss")
        pygame.event.clear()


# Function to update and draw all sprites
def update_and_draw_sprites():
    player_group.draw(screen)
    aliens.draw(screen)
    boss_group.draw(screen)
    player_projectiles.draw(screen)
    alien_projectiles.draw(screen)

    # Update all sprites
    keys = pygame.key.get_pressed()
    player_group.update(keys)
    aliens.update()
    boss_group.update()
    player_projectiles.update()
    alien_projectiles.update()


# Function to handle collisions
def handle_collisions():
    global score, no_life_lost

    # Player projectiles hitting aliens
    hits = pygame.sprite.groupcollide(aliens, player_projectiles, True, True)
    if hits:
        for hit in hits:
            score += 10
            play_sound(kill_sound)

    # Player projectiles hitting boss
    if boss_group:
        boss = boss_group.sprites()[0]
        boss_hits = pygame.sprite.spritecollide(boss, player_projectiles, True)
        for hit in boss_hits:
            boss.health -= 1
            score += 50
            play_sound(kill_sound)
            if boss.health <= 0:
                boss.kill()
                score += 100
                if no_life_lost:
                    player.gain_life()

    # Alien projectiles hitting player
    if pygame.sprite.spritecollide(player, alien_projectiles, True):
        player.lose_life()
        no_life_lost = False

    # Aliens reaching bottom
    for alien in aliens:
        if alien.rect.bottom >= SCREEN_HEIGHT - 50:
            player.lose_life()
            alien.kill()
            no_life_lost = False


# Function to handle alien shooting
def handle_alien_shooting():
    global last_alien_shot
    now = pygame.time.get_ticks()
    if now - last_alien_shot > alien_shoot_interval and aliens:
        shooting_alien = random.choice(aliens.sprites())
        if len(alien_projectiles) < 20:
            shooting_alien.shoot()
        last_alien_shot = now


# Function to display score and lives
def display_score_and_lives():
    score_text = FONT.render(f"Score: {score}", True, NEON_GREEN)
    lives_text = FONT.render(f"Lives: {player.lives}", True, NEON_GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, SCREEN_HEIGHT - 50))


# Function to handle boss background
def handle_background():
    if boss_group:
        screen.blit(boss_bg, (0, 0))
    else:
        screen.blit(normal_bg, (0, 0))


# Main Game Loop
clock = pygame.time.Clock()

# Initial spawn of aliens
spawn_aliens()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if game_state == "GAME":
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.shoot()

    if game_state == "MENU":
        state = display_menu()
        if state != "MENU":
            game_state = state

    elif game_state == "INSTRUCTIONS":
        state = display_instructions()
        if state != "INSTRUCTIONS":
            game_state = state

    elif game_state == "GAME":
        handle_background()

        # Handle shooting by aliens
        handle_alien_shooting()

        # Update and draw all sprites
        update_and_draw_sprites()

        # Handle collisions
        handle_collisions()

        # Handle level progression
        handle_level_progression()

        # Display score and lives
        display_score_and_lives()

    elif game_state == "GAME_OVER":
        state = display_game_over()
        if state != "GAME_OVER":
            game_state = state

    pygame.display.flip()

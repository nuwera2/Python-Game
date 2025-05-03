
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
FONT = pygame.font.SysFont('arial', 24)

MAX_HEALTH = 100
TRAP_DAMAGE = 20
POTION_HEAL = 15
TARGET_GOLD = 50

# --- Game State ---
health = MAX_HEALTH
gold = 0
message = "Click 'Roll' to begin your quest!"

# --- Screen Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mystic Dice Quest")

# --- Button Setup ---
roll_button = pygame.Rect(WIDTH//2 - 50, HEIGHT - 80, 100, 40)

def roll_die():
    return random.randint(1, 6)

def encounter():
    global health, gold, message

    roll = roll_die()
    message = f"You rolled a {roll}!"

    if roll <= 2:
        health -= TRAP_DAMAGE
        message += f" Trap! -{TRAP_DAMAGE} HP."
    elif roll <= 4:
        message += " Nothing happened."
    elif roll == 5:
        gold += 10
        message += " You found 10 gold!"
    elif roll == 6:
        heal = min(POTION_HEAL, MAX_HEALTH - health)
        health += heal
        message += f" You found a potion. +{heal} HP."

def draw_text(text, x, y, color=BLACK):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_game():
    screen.fill(WHITE)

    # Health and Gold
    draw_text(f"Health: {health}/{MAX_HEALTH}", 30, 30)
    draw_text(f"Gold: {gold}/{TARGET_GOLD}", 30, 70)

    # Game message
    draw_text(message, 30, 120)

    # Roll Button
    pygame.draw.rect(screen, GREEN, roll_button)
    draw_text("ROLL", roll_button.x + 20, roll_button.y + 5)

    pygame.display.flip()

def game_over(win):
    screen.fill(WHITE)
    msg = "🎉 You win!" if win else "💀 You lose!"
    draw_text(msg, WIDTH//2 - 60, HEIGHT//2 - 20)
    draw_text("Press any key to exit.", WIDTH//2 - 120, HEIGHT//2 + 20)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
    pygame.quit()
    sys.exit()

# --- Main Loop ---
running = True
while running:
    draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if roll_button.collidepoint(event.pos):
                encounter()
                if health <= 0:
                    game_over(win=False)
                elif gold >= TARGET_GOLD:
                    game_over(win=True)

pygame.quit()

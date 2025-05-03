import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 600, 500
FPS = 30

# Colors
BG_COLOR = (30, 30, 30)
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 215, 0)
BUTTON_COLOR = (50, 50, 200)
BUTTON_HOVER = (80, 80, 255)
TEXT_COLOR = WHITE

# Game constants
MAX_HEALTH = 100
TRAP_DAMAGE = 20
POTION_HEAL = 15
TARGET_GOLD = 50

# --- Game State ---
health = MAX_HEALTH
gold = 0
message = "Click ROLL to begin!"

# --- Pygame Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mystic Dice Quest - Enhanced")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

# Button
roll_button = pygame.Rect(WIDTH//2 - 60, HEIGHT - 80, 120, 50)

# Dice pip positions
pip_map = {
    1: [(0.5,0.5)],
    2: [(0.25,0.25),(0.75,0.75)],
    3: [(0.25,0.25),(0.5,0.5),(0.75,0.75)],
    4: [(0.25,0.25),(0.25,0.75),(0.75,0.25),(0.75,0.75)],
    5: [(0.25,0.25),(0.25,0.75),(0.5,0.5),(0.75,0.25),(0.75,0.75)],
    6: [(0.25,0.25),(0.25,0.5),(0.25,0.75),(0.75,0.25),(0.75,0.5),(0.75,0.75)],
}

def draw_text(text, x, y, color=TEXT_COLOR):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

def draw_bars():
    # Health bar
    bar_width = WIDTH - 60
    pygame.draw.rect(screen, RED, (30, 30, bar_width, 20))
    health_width = int(bar_width * (health / MAX_HEALTH))
    pygame.draw.rect(screen, GREEN, (30, 30, health_width, 20))
    draw_text(f"HP: {health}/{MAX_HEALTH}", 40, 55)
    # Gold bar
    pygame.draw.rect(screen, BLACK, (30, 90, bar_width, 20))
    gold_width = int(bar_width * (gold / TARGET_GOLD))
    pygame.draw.rect(screen, YELLOW, (30, 90, gold_width, 20))
    draw_text(f"Gold: {gold}/{TARGET_GOLD}", 40, 115)

def draw_dice(face):
    size = 100
    rect = pygame.Rect(WIDTH//2 - size//2, HEIGHT//2 - size//2, size, size)
    pygame.draw.rect(screen, WHITE, rect, border_radius=8)
    radius = int(size * 0.07)
    for ox, oy in pip_map[face]:
        cx = rect.x + int(ox * size)
        cy = rect.y + int(oy * size)
        pygame.draw.circle(screen, BLACK, (cx, cy), radius)

def roll_animation():
    # Animate random faces briefly
    for _ in range(FPS//2):
        face = random.randint(1, 6)
        screen.fill(BG_COLOR)
        draw_bars()
        draw_text(message, 30, HEIGHT//2 + 80)
        draw_dice(face)
        mx, my = pygame.mouse.get_pos()
        btn_color = BUTTON_HOVER if roll_button.collidepoint((mx,my)) else BUTTON_COLOR
        pygame.draw.rect(screen, btn_color, roll_button, border_radius=8)
        draw_text("ROLL", roll_button.x+30, roll_button.y+10)
        pygame.display.flip()
        clock.tick(FPS)

def encounter():
    global health, gold, message
    roll = random.randint(1, 6)
    message = f"You rolled a {roll}!"
    if roll <= 2:
        health -= TRAP_DAMAGE
        message += f" Trap! -{TRAP_DAMAGE} HP."
    elif roll <= 4:
        message += " Nothing happens."
    elif roll == 5:
        gold += 10
        message += " +10 gold!"
    else:
        heal = min(POTION_HEAL, MAX_HEALTH - health)
        health += heal
        message += f" Potion! +{heal} HP."

def game_over(win):
    screen.fill(BG_COLOR)
    msg = "🎉 You Win!" if win else "💀 Game Over"
    draw_text(msg, WIDTH//2 - 80, HEIGHT//2 - 20)
    draw_text("Press any key to exit.", WIDTH//2 - 130, HEIGHT//2 + 20)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
    pygame.quit()
    sys.exit()

# Main game loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_bars()
    draw_text(message, 30, HEIGHT//2 + 80)
    draw_dice(1)  # default face
    mx, my = pygame.mouse.get_pos()
    btn_color = BUTTON_HOVER if roll_button.collidepoint((mx,my)) else BUTTON_COLOR
    pygame.draw.rect(screen, btn_color, roll_button, border_radius=8)
    draw_text("ROLL", roll_button.x+30, roll_button.y+10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and roll_button.collidepoint(event.pos):
            roll_animation()
            encounter()
            if health <= 0:
                game_over(False)
            elif gold >= TARGET_GOLD:
                game_over(True)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()




   
   

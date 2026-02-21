import pygame
import sys
import random

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MindState")

font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (60, 60, 60)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)

clock = pygame.time.Clock()

# Player & NPC Stats
stability = 70

npc = {
    "trust": 50,
    "fear": 20,
    "respect": 30
}

# Animated display values
display_trust = npc["trust"]
display_fear = npc["fear"]
display_respect = npc["respect"]
display_stability = stability

shake_timer = 0
shake_offset = [0, 0]
flash_alpha = 0

message = "NPC: Why did you ignore my call yesterday?"

choices = [
    ("Calm: I needed space.", "calm"),
    ("Aggressive: Stop overreacting.", "aggressive"),
    ("Supportive: I’m sorry, I was stressed.", "supportive")
]

def update_stats(choice_type):
    global stability, shake_timer, flash_alpha

    if choice_type == "calm":
        npc["trust"] += 5
        npc["respect"] += 3
        stability += 2

    elif choice_type == "aggressive":
        npc["fear"] += 10
        npc["trust"] -= 5
        stability -= 8
        shake_timer = 15
        flash_alpha = 120

    elif choice_type == "supportive":
        npc["trust"] += 8
        npc["fear"] -= 5
        stability += 5

def draw_bar(x, y, value, max_value, color):
    pygame.draw.rect(screen, GRAY, (x, y, 200, 20))
    fill_width = (value / max_value) * 200
    pygame.draw.rect(screen, color, (x, y, fill_width, 20))

def draw_stats():
    screen.blit(font.render("Trust", True, WHITE), (50 + shake_offset[0], 50 + shake_offset[1]))
    draw_bar(150 + shake_offset[0], 55 + shake_offset[1], display_trust, 100, GREEN)

    screen.blit(font.render("Fear", True, WHITE), (50 + shake_offset[0], 85 + shake_offset[1]))
    draw_bar(150 + shake_offset[0], 90 + shake_offset[1], display_fear, 100, RED)

    screen.blit(font.render("Respect", True, WHITE), (50 + shake_offset[0], 120 + shake_offset[1]))
    draw_bar(150 + shake_offset[0], 125 + shake_offset[1], display_respect, 100, BLUE)

    screen.blit(font.render("Stability", True, WHITE), (50 + shake_offset[0], 155 + shake_offset[1]))
    draw_bar(150 + shake_offset[0], 160 + shake_offset[1], display_stability, 100, WHITE)

def draw_choices():
    y_offset = 350
    for i, choice in enumerate(choices):
        text = font.render(f"{i+1}. {choice[0]}", True, WHITE)
        screen.blit(text, (50 + shake_offset[0], y_offset + shake_offset[1]))
        y_offset += 40

running = True

while running:
    clock.tick(60)

    # Smooth animation toward real values
    display_trust += (npc["trust"] - display_trust) * 0.1
    display_fear += (npc["fear"] - display_fear) * 0.1
    display_respect += (npc["respect"] - display_respect) * 0.1
    display_stability += (stability - display_stability) * 0.1

    # Screen Shake Logic
    if shake_timer > 0:
        shake_offset[0] = random.randint(-5, 5)
        shake_offset[1] = random.randint(-5, 5)
        shake_timer -= 1
    else:
        shake_offset = [0, 0]

    screen.fill(BLACK)

    screen.blit(big_font.render("MindState", True, WHITE), (WIDTH//2 - 80 + shake_offset[0], 20 + shake_offset[1]))
    screen.blit(font.render(message, True, WHITE), (50 + shake_offset[0], 250 + shake_offset[1]))

    draw_stats()
    draw_choices()

    # Red Flash Overlay
    if flash_alpha > 0:
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.set_alpha(flash_alpha)
        flash.fill((255, 0, 0))
        screen.blit(flash, (0, 0))
        flash_alpha -= 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                update_stats(choices[0][1])
            if event.key == pygame.K_2:
                update_stats(choices[1][1])
            if event.key == pygame.K_3:
                update_stats(choices[2][1])

    pygame.display.flip()

pygame.quit()
sys.exit()
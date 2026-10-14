
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
FPS = 12

# Colors
BLACK = (18, 18, 25)
WHITE = (245, 245, 245)
GREEN = (0, 220, 100)
DARK_GREEN = (0, 150, 70)
RED = (255, 75, 75)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 110)

# Fonts
font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 18)
big_font = pygame.font.SysFont("Arial", 42, bold=True)


def draw_text(text, font_obj, color, x, y, center=True):
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(surface, rect)


def random_food(snake):
    while True:
        food = (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE),
        )
        if food not in snake:
            return food


def reset_game():
    snake = [
        (WIDTH // 2, HEIGHT // 2),
        (WIDTH // 2 - CELL_SIZE, HEIGHT // 2),
        (WIDTH // 2 - 2 * CELL_SIZE, HEIGHT // 2),
    ]

    direction = (CELL_SIZE, 0)
    food = random_food(snake)
    score = 0

    return snake, direction, food, score


def draw_game(snake, food, score, high_score):
    screen.fill(BLACK)

    # Draw food
    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], CELL_SIZE, CELL_SIZE),
        border_radius=5,
    )

    # Draw snake
    for index, segment in enumerate(snake):
        color = GREEN if index == 0 else DARK_GREEN

        pygame.draw.rect(
            screen,
            color,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
            border_radius=4,
        )

    # Score display
    draw_text(
        f"Score: {score}",
        font,
        WHITE,
        10,
        10,
        center=False,
    )

    draw_text(
        f"Best: {high_score}",
        small_font,
        YELLOW,
        WIDTH - 100,
        15,
        center=False,
    )

    # Border
    pygame.draw.rect(
        screen,
        GRAY,
        (0, 0, WIDTH, HEIGHT),
        2,
    )

    pygame.display.flip()


def game_over_screen(score, high_score):
    while True:
        screen.fill(BLACK)

        draw_text("GAME OVER", big_font, RED, WIDTH // 2, 100)
        draw_text(f"Your Score: {score}", font, WHITE, WIDTH // 2, 165)
        draw_text(f"Best Score: {high_score}", font, YELLOW, WIDTH // 2, 205)

        draw_text(
            "Press R to Restart",
            small_font,
            GREEN,
            WIDTH // 2,
            270,
        )
        draw_text(
            "Press Q or ESC to Quit",
            small_font,
            WHITE,
            WIDTH // 2,
            305,
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        clock.tick(30)


def main():
    high_score = 0

    while True:
        snake, direction, food, score = reset_game()
        next_direction = direction
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Prevent reversing directly into yourself
                    if event.key in (pygame.K_UP, pygame.K_w):
                        if direction[1] == 0:
                            next_direction = (0, -CELL_SIZE)

                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        if direction[1] == 0:
                            next_direction = (0, CELL_SIZE)

                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if direction[0] == 0:
                            next_direction = (-CELL_SIZE, 0)

                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if direction[0] == 0:
                            next_direction = (CELL_SIZE, 0)

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            direction = next_direction

            # Calculate new head position
            head_x = snake[0][0] + direction[0]
            head_y = snake[0][1] + direction[1]
            new_head = (head_x, head_y)

            # Wall collision
            head_x = head_x % WIDTH
            head_y = head_y % HEIGHT

            new_head = (head_x, head_y)

            # Check whether the snake eats food
            eating = new_head == food

            # The tail moves away unless food is eaten
            body_to_check = snake if eating else snake[:-1]

            # Self collision
            if new_head in body_to_check:
                running = False
                break

            snake.insert(0, new_head)

            if eating:
                score += 10
                high_score = max(high_score, score)
                food = random_food(snake)
            else:
                snake.pop()

            draw_game(snake, food, score, high_score)
            clock.tick(FPS)

        game_over_screen(score, high_score)


if __name__ == "__main__":
    main()
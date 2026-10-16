import pygame
from Engine import create_grid

TILE_SIZE = 60
PADDING = 20

BACKGROUND = (35, 35, 40)
HIDDEN_COLOR = (100, 110, 125)
REVEALED_COLOR = (205, 210, 215)
MINE_COLOR = (220, 70, 70)
TEXT_COLOR = (30, 30, 30)
FLAG_COLOR = (255, 80, 80)

NUMBER_COLORS = {
    1: (30, 90, 220),
    2: (30, 140, 70),
    3: (220, 50, 50),
    4: (100, 50, 180),
    5: (160, 80, 30),
    6: (30, 150, 160),
    7: (30, 30, 30),
    8: (100, 100, 100),
}


def reveal_cell(grid, revealed, i, j):
    """Reveal a safe cell and expand connected zero cells."""
    size = len(grid)
    stack = [(i, j)]

    while stack:
        r, c = stack.pop()

        if not (0 <= r < size and 0 <= c < size):
            continue

        if (r, c) in revealed:
            continue

        if grid[r][c] == "M":
            continue

        revealed.add((r, c))

        if grid[r][c] != 0:
            continue

        for nr in range(max(0, r - 1), min(size, r + 2)):
            for nc in range(max(0, c - 1), min(size, c + 2)):
                if (nr, nc) != (r, c):
                    stack.append((nr, nc))


def game():
    pygame.init()

    grid = create_grid()
    size = len(grid)

    screen_width = size * TILE_SIZE + PADDING * 2
    screen_height = size * TILE_SIZE + PADDING * 2 + 50

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Minesweeper")

    revealed = set()
    flags = set()

    game_over = False
    won = False
    running = True

    font = pygame.font.Font(None, 32)
    message_font = pygame.font.Font(None, 28)

    clock = pygame.time.Clock()

    total_safe_cells = sum(1 for row in grid for cell in row if cell != "M")

    total_mines = sum(1 for row in grid for cell in row if cell == "M")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and not game_over
            ):
                mx, my = event.pos

                j = (mx - PADDING) // TILE_SIZE
                i = (my - PADDING) // TILE_SIZE

                inside_board = (
                    PADDING <= mx < PADDING + size * TILE_SIZE
                    and PADDING <= my < PADDING + size * TILE_SIZE
                )

                if inside_board and (i, j) not in revealed and (i, j) not in flags:
                    if grid[i][j] == "M":
                        game_over = True
                        won = False

                        revealed.update(
                            (r, c)
                            for r, row in enumerate(grid)
                            for c, cell in enumerate(row)
                            if cell == "M"
                        )

                    else:
                        reveal_cell(grid, revealed, i, j)

                        if len(revealed) == total_safe_cells:
                            game_over = True
                            won = True

            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 3
                and not game_over
            ):
                mx, my = event.pos

                j = (mx - PADDING) // TILE_SIZE
                i = (my - PADDING) // TILE_SIZE

                inside_board = (
                    PADDING <= mx < PADDING + size * TILE_SIZE
                    and PADDING <= my < PADDING + size * TILE_SIZE
                )

                if inside_board and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))

        screen.fill(BACKGROUND)

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x = PADDING + j * TILE_SIZE
                y = PADDING + i * TILE_SIZE

                rect = pygame.Rect(x, y, TILE_SIZE - 2, TILE_SIZE - 2)

                if (i, j) in revealed:
                    if cell == "M" and (i, j) in flags:
                        color = (50, 200, 80)  
                    elif cell == "M":
                        color = MINE_COLOR    
                    else:
                        color = REVEALED_COLOR

                    pygame.draw.rect(screen, color, rect)

                    if cell == "M":
                        text_value = "M"
                        text_color = (255, 255, 255)
                    else:
                        text_value = str(cell)
                        text_color = NUMBER_COLORS.get(cell, TEXT_COLOR)

                    if cell != 0:
                        text = font.render(text_value, True, text_color)
                        screen.blit(text, text.get_rect(center=rect.center))

                else:
                    pygame.draw.rect(screen, HIDDEN_COLOR, rect)

                    if (i, j) in flags:
                        flag_text = font.render("F", True, FLAG_COLOR)
                        screen.blit(flag_text, flag_text.get_rect(center=rect.center))

        remaining = total_mines - len(flags)
        counter_text = message_font.render(
            f"Flags remaining: {remaining}", True, (240, 240, 240)
        )
        screen.blit(counter_text, (PADDING, size * TILE_SIZE + PADDING + 12))

        if game_over:
            message = "YOU WIN!" if won else "GAME OVER!"
            color = (80, 220, 100) if won else (255, 90, 90)

            result_text = message_font.render(message, True, color)
            screen.blit(
                result_text,
                result_text.get_rect(
                    center=(screen_width // 2, size * TILE_SIZE + PADDING + 35)
                ),
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game()

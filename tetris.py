import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]


class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        self.current_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        piece = random.choice(SHAPES)
        color = random.choice([RED, CYAN, MAGENTA, YELLOW, GREEN, BLUE, ORANGE])
        return {'piece': piece, 'color': color, 'row': 0, 'col': GRID_WIDTH // 2 - len(piece[0]) // 2}

    def draw_grid(self):
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col] != 0:
                    pygame.draw.rect(self.screen, self.grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_piece(self, piece):
        for row in range(len(piece['piece'])):
            for col in range(len(piece['piece'][0])):
                if piece['piece'][row][col] == 1:
                    pygame.draw.rect(self.screen, piece['color'],
                                     ((col + piece['col']) * GRID_SIZE, (row + piece['row']) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE,
                                     ((col + piece['col']) * GRID_SIZE, (row + piece['row']) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def check_collision(self, piece):
        for row in range(len(piece['piece'])):
            for col in range(len(piece['piece'][0])):
                if piece['piece'][row][col] == 1:
                    if piece['row'] + row >= GRID_HEIGHT or piece['col'] + col < 0 or piece['col'] + col >= GRID_WIDTH or \
                            self.grid[piece['row'] + row][piece['col'] + col] != 0:
                        return True
        return False

    def lock_piece(self, piece):
        for row in range(len(piece['piece'])):
            for col in range(len(piece['piece'][0])):
                if piece['piece'][row][col] == 1:
                    self.grid[piece['row'] + row][piece['col'] + col] = piece['color']

    def clear_lines(self):
        lines_to_clear = [row for row in range(GRID_HEIGHT) if all(self.grid[row])]
        for row in lines_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * GRID_WIDTH)

    def rotate_piece(self, piece):
        rotated_piece = list(zip(*reversed(piece['piece'])))
        if piece['col'] + len(rotated_piece[0]) > GRID_WIDTH:
            return piece
        return {'piece': rotated_piece, 'color': piece['color'], 'row': piece['row'], 'col': piece['col']}

    def move_piece(self, piece, direction):
        new_col = piece['col'] + direction
        if 0 <= new_col < GRID_WIDTH and not self.check_collision({'piece': piece['piece'], 'color': piece['color'], 'row': piece['row'], 'col': new_col}):
            piece['col'] = new_col
        return piece

    def drop_piece(self, piece):
        while not self.check_collision({'piece': piece['piece'], 'color': piece['color'], 'row': piece['row'] + 1, 'col': piece['col']}):
            piece['row'] += 1
        return piece

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece = self.move_piece(self.current_piece, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece = self.move_piece(self.current_piece, 1)
                    elif event.key == pygame.K_DOWN:
                        self.current_piece = self.drop_piece(self.current_piece)
                    elif event.key == pygame.K_UP:
                        self.current_piece = self.rotate_piece(self.current_piece)

            # Move the piece down periodically
            if not self.check_collision({'piece': self.current_piece['piece'], 'color': self.current_piece['color'], 'row': self.current_piece['row'] + 1, 'col': self.current_piece['col']}):
                self.current_piece['row'] += 1
            else:
                self.lock_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.new_piece()
                if self.check_collision(self.current_piece):
                    self.game_over = True

            # Clear the screen
            self.screen.fill(BLACK)

            # Draw the grid and the current piece
            self.draw_grid()
            self.draw_piece(self.current_piece)

            # Update the display
            pygame.display.flip()

            # Set the frames per second
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
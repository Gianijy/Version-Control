# snake.py
import sys, random, pygame

# ------------------ Config ------------------
CELL       = 16                 # pixel size of one grid cell
GRID_W     = 46                 # number of columns
GRID_H     = 26                 # number of rows
BORDER     = 10                 # outer frame thickness (pixels)
FPS_START  = 10                 # initial speed
FPS_STEP   = 0.25               # speed up per food eaten
WINDOW_W   = GRID_W * CELL + BORDER * 2
WINDOW_H   = GRID_H * CELL + BORDER * 2

# Colors
BLACK      = (0, 0, 0)
INK        = (10, 36, 52)       # dark blue-ish frame (like screenshot)
GREEN      = (80, 220, 60)
GREEN_DARK = (40, 180, 30)
RED        = (220, 40, 40)
WHITE      = (240, 240, 240)

# ------------------ Helpers ------------------
def grid_to_px(col, row):
    """Convert grid coords to pixel rect (x, y, w, h)."""
    x = BORDER + col * CELL
    y = BORDER + row * CELL
    return pygame.Rect(x, y, CELL, CELL)

def random_open_cell(occupied):
    """Pick a random free cell not in occupied set."""
    while True:
        c = random.randrange(GRID_W)
        r = random.randrange(GRID_H)
        if (c, r) not in occupied:
            return (c, r)

# ------------------ Game Objects ------------------
class Snake:
    def __init__(self):
        midx = GRID_W // 4
        midy = GRID_H // 2
        self.body = [(midx + i, midy) for i in range(3, -1, -1)]  # head = body[0]
        self.dir = (1, 0)  # moving right
        self.grow = 0

    def head(self):
        return self.body[0]

    def set_dir(self, newdir):
        # Prevent immediate 180° turns
        if (newdir[0] == -self.dir[0] and newdir[1] == -self.dir[1]):
            return
        self.dir = newdir

    def step(self):
        hx, hy = self.head()
        nx, ny = hx + self.dir[0], hy + self.dir[1]
        new_head = (nx, ny)

        # Collision with walls?
        if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H:
            return False  # dead

        # Collision with itself?
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()
        return True

    def eat(self):
        self.grow += 1

    def draw(self, surf):
        # Draw body with a bright head and darker body + subtle inner highlight
        for i, (x, y) in enumerate(self.body):
            rect = grid_to_px(x, y)
            color = GREEN if i == 0 else GREEN_DARK
            pygame.draw.rect(surf, color, rect)
            inner = rect.inflate(-4, -4)
            pygame.draw.rect(surf, (0, 0, 0), inner, width=0)  # inner black for pixelated look
            inner2 = rect.inflate(-6, -6)
            pygame.draw.rect(surf, color, inner2, width=0)

# ------------------ Main Game ------------------
def run():
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas,menlo,monaco,dejavusansmono", 18, bold=True)

    def new_round():
        snake = Snake()
        occupied = set(snake.body)
        food = random_open_cell(occupied)
        fps = FPS_START
        score = 0
        paused = False
        alive = True
        return snake, food, fps, score, paused, alive

    snake, food, fps, score, paused, alive = new_round()

    while True:
        # -------- events ----------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_p:
                    paused = not paused
                if not alive and e.key == pygame.K_r:
                    snake, food, fps, score, paused, alive = new_round()
                # movement
                if e.key in (pygame.K_LEFT, pygame.K_a):
                    snake.set_dir((-1, 0))
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.set_dir((1, 0))
                elif e.key in (pygame.K_UP, pygame.K_w):
                    snake.set_dir((0, -1))
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    snake.set_dir((0, 1))

        # -------- update ----------
        if alive and not paused:
            if not snake.step():
                alive = False
            else:
                # eat?
                if snake.head() == food:
                    snake.eat()
                    score += 1
                    fps = min(60, FPS_START + score * FPS_STEP)
                    occupied = set(snake.body)
                    food = random_open_cell(occupied)

        # -------- draw ----------
        screen.fill(INK)  # frame
        # board area
        board_rect = pygame.Rect(BORDER, BORDER, GRID_W * CELL, GRID_H * CELL)
        pygame.draw.rect(screen, BLACK, board_rect)

        # food
        pygame.draw.rect(screen, RED, grid_to_px(*food))

        # snake
        snake.draw(screen)

        # hud
        txt = f"Score: {score}    Speed: {fps:.1f} FPS"
        surf = font.render(txt, True, WHITE)
        screen.blit(surf, (BORDER, 4))

        if paused:
            pmsg = font.render("PAUSED (P to resume)", True, WHITE)
            screen.blit(pmsg, (WINDOW_W // 2 - pmsg.get_width() // 2, 4))

        if not alive:
            g1 = font.render("GAME OVER", True, WHITE)
            g2 = font.render("Press R to restart  •  Esc to quit", True, WHITE)
            screen.blit(g1, (WINDOW_W // 2 - g1.get_width() // 2, WINDOW_H // 2 - 20))
            screen.blit(g2, (WINDOW_W // 2 - g2.get_width() // 2, WINDOW_H // 2 + 6))

        pygame.display.flip()
        clock.tick(fps if alive and not paused else 60)

if __name__ == "__main__":
    run()
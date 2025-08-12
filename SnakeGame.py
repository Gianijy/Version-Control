# smooth_snake.py
import sys, random, copy, pygame

# ===================== Config =====================
CELL       = 22                   # size of a grid cell in pixels
GRID_W     = 42                   # columns
GRID_H     = 24                   # rows
BORDER     = 12                   # outer frame thickness
WINDOW_W   = GRID_W * CELL + BORDER * 2
WINDOW_H   = GRID_H * CELL + BORDER * 2

SNAKE_LEN0 = 6                    # starting length
SPEED      = 6.0                  # cells per second (base)
SPEED_GAIN = 0.10                 # add per fruit eaten
MAX_SPEED  = 12.0

# Colors
INK        = (10, 36, 52)
BOARD      = (0, 0, 0)
HEAD_COL   = (120, 255, 90)
BODY_COL   = (70, 210, 60)
HUD        = (240, 240, 240)

# ===================== Helpers =====================
def cell_rect(col, row):
    x = BORDER + col * CELL
    y = BORDER + row * CELL
    return pygame.Rect(x, y, CELL, CELL)

def clamp(v, a, b): return a if v < a else b if v > b else v

# ===================== Fruits ======================
FRUITS = ("apple", "cherry", "lemon", "grape")

def draw_fruit(surf, kind, col, row):
    """Simple procedural fruit sprites."""
    r = cell_rect(col, row)
    cx, cy = r.center
    # shrink to avoid touching cell edges
    radius = int(CELL * 0.38)

    if kind == "apple":
        # body
        pygame.draw.circle(surf, (220, 40, 40), (cx, cy), radius)
        # highlight
        pygame.draw.circle(surf, (255, 120, 120), (cx - radius//3, cy - radius//3), radius//3)
        # stem
        pygame.draw.line(surf, (90, 60, 20), (cx, cy - radius), (cx, cy - radius - 6), 3)
        # leaf
        pygame.draw.circle(surf, (40, 170, 70), (cx + 6, cy - radius - 2), 5)

    elif kind == "cherry":
        # two cherries
        pygame.draw.circle(surf, (210, 20, 50), (cx - 6, cy), radius-3)
        pygame.draw.circle(surf, (210, 20, 50), (cx + 8, cy - 4), radius-3)
        # stems
        pygame.draw.line(surf, (90, 60, 20), (cx - 6, cy - (radius-3)), (cx + 3, cy - radius - 8), 2)
        pygame.draw.line(surf, (90, 60, 20), (cx + 8, cy - (radius-3) - 4), (cx + 3, cy - radius - 8), 2)
        # leaf
        pygame.draw.circle(surf, (40, 170, 70), (cx + 8, cy - radius - 8), 5)

    elif kind == "lemon":
        # oval
        lemon_rect = pygame.Rect(0,0, int(radius*2.1), int(radius*1.4))
        lemon_rect.center = (cx, cy)
        pygame.draw.ellipse(surf, (245, 210, 60), lemon_rect)
        # highlight
        hi = lemon_rect.copy(); hi.inflate_ip(-lemon_rect.w*0.55, -lemon_rect.h*0.55)
        pygame.draw.ellipse(surf, (255, 245, 140), hi)
        # stem/leaf
        pygame.draw.line(surf, (90,60,20), (cx, lemon_rect.top), (cx, lemon_rect.top-5), 2)
        pygame.draw.circle(surf, (40,170,70), (cx+6, lemon_rect.top-5), 5)

    else: # grape
        # cluster
        purple = (150, 50, 200)
        offsets = [(-6,2),(0,0),(6,2),(-3,8),(3,8),(0,14)]
        for ox, oy in offsets:
            pygame.draw.circle(surf, purple, (cx+ox, cy+oy), radius-8)
        # leaf
        pygame.draw.circle(surf, (40,170,70), (cx-2, cy - radius - 3), 5)
        pygame.draw.line(surf, (90,60,20), (cx-2, cy - radius - 3), (cx, cy - 10), 2)

# ================== Snake (grid logic + smooth draw) ==================
class Snake:
    def __init__(self):
        my = GRID_H // 2
        mx = GRID_W // 3
        self.cells = [(mx - i, my) for i in range(SNAKE_LEN0)]  # [head,...,tail]
        self.prev_cells = copy.deepcopy(self.cells)             # for interpolation
        self.dir = (1, 0)                                      # moving right
        self.grow = 0

    def head(self): return self.cells[0]

    def set_dir(self, d):
        # block immediate reversal
        if (d[0] == -self.dir[0] and d[1] == -self.dir[1]):
            return
        # also prevent changing axis twice in one tick (feels more natural)
        self.dir = d

    def step(self):
        hx, hy = self.cells[0]
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        # wall collision
        if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H:
            return False

        # self collision
        if (nx, ny) in self.cells:
            return False

        self.prev_cells = copy.deepcopy(self.cells)  # for smooth draw
        self.cells.insert(0, (nx, ny))
        if self.grow > 0:
            self.grow -= 1
        else:
            self.cells.pop()
        return True

    def eat(self): self.grow += 1

    def draw_smooth(self, surf, t):
        """t in [0,1]: interpolate from prev_cells -> cells."""
        # Rounded rectangles for segments, brighter head
        for idx in range(len(self.cells)):
            # for the tail, prev list may be longer when growing; guard indexes
            if idx >= len(self.prev_cells):
                a = self.cells[idx]
                b = a
            else:
                a = self.prev_cells[idx]
                b = self.cells[idx]

            x = (1-t)*a[0] + t*b[0]
            y = (1-t)*a[1] + t*b[1]
            rect = cell_rect(x, y)  # accept floats

            # draw rounded pill
            color = HEAD_COL if idx == 0 else BODY_COL
            pygame.draw.rect(surf, color, rect, border_radius=int(CELL*0.3))
            # subtle inner shade
            inner = rect.inflate(-6, -6)
            pygame.draw.rect(surf, (0,0,0), inner, border_radius=int(CELL*0.25))

def cell_rect(colf, rowf):
    """Float-friendly rect for smooth interpolation."""
    x = BORDER + colf * CELL
    y = BORDER + rowf * CELL
    return pygame.Rect(int(x), int(y), CELL, CELL)

# ===================== Game Loop =====================
def run():
    pygame.init()
    pygame.display.set_caption("Smooth Snake")
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas,menlo,monaco,dejavusansmono", 18, bold=True)

    def new_game():
        snake = Snake()
        occupied = set(snake.cells)
        food_pos = random_free_cell(occupied)
        food_kind = random.choice(FRUITS)
        speed = SPEED
        score = 0
        alive = True
        paused = False
        # smooth mover
        prog = 0.0    # progress 0..1 between steps
        return snake, food_pos, food_kind, speed, score, alive, paused, prog

    def random_free_cell(blocked):
        while True:
            c = random.randrange(GRID_W)
            r = random.randrange(GRID_H)
            if (c, r) not in blocked:
                return (c, r)

    snake, food_pos, food_kind, speed, score, alive, paused, prog = new_game()

    while True:
        dt = clock.tick(120) / 1000.0  # high FPS for smoothness

        # ---- events ----
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q): pygame.quit(); sys.exit()
                if e.key == pygame.K_p: paused = not paused
                if not alive and e.key == pygame.K_r:
                    snake, food_pos, food_kind, speed, score, alive, paused, prog = new_game()
                # movement
                if e.key in (pygame.K_LEFT, pygame.K_a):  snake.set_dir((-1, 0))
                if e.key in (pygame.K_RIGHT, pygame.K_d): snake.set_dir((1, 0))
                if e.key in (pygame.K_UP, pygame.K_w):    snake.set_dir((0, -1))
                if e.key in (pygame.K_DOWN, pygame.K_s):  snake.set_dir((0, 1))

        # ---- update ----
        if alive and not paused:
            prog += speed * dt  # cells per second
            while prog >= 1.0:
                prog -= 1.0
                if not snake.step():
                    alive = False
                    break
                # eat?
                if snake.head() == food_pos:
                    snake.eat()
                    score += 1
                    speed = clamp(speed + SPEED_GAIN, SPEED, MAX_SPEED)
                    occupied = set(snake.cells)
                    food_pos = random_free_cell(occupied)
                    food_kind = random.choice(FRUITS)

        # ---- draw ----
        screen.fill(INK)
        board_rect = pygame.Rect(BORDER, BORDER, GRID_W*CELL, GRID_H*CELL)
        pygame.draw.rect(screen, BOARD, board_rect)

        # fruit
        draw_fruit(screen, food_kind, *food_pos)

        # snake (smooth interpolation)
        snake.draw_smooth(screen, prog if (alive and not paused) else 0.0)

        # HUD
        hud = font.render(f"Score: {score}   Speed: {speed:.1f}", True, HUD)
        screen.blit(hud, (BORDER, 4))
        if paused:
            p = font.render("PAUSED (P to resume)", True, HUD)
            screen.blit(p, (WINDOW_W//2 - p.get_width()//2, 4))
        if not alive:
            g1 = font.render("GAME OVER", True, HUD)
            g2 = font.render("Press R to restart • Esc to quit", True, HUD)
            screen.blit(g1, (WINDOW_W//2 - g1.get_width()//2, WINDOW_H//2 - 16))
            screen.blit(g2, (WINDOW_W//2 - g2.get_width()//2, WINDOW_H//2 + 10))

        pygame.display.flip()

if __name__ == "__main__":
    run()
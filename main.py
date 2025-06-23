import pygame
import pygame_menu
from queue import PriorityQueue, Queue
import sys

pygame.init()

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("The Pathfinder")

# Colors
RED = (255, 0, 0)        # End
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)  # Barrier
BLACK = (0, 0, 0)        # Empty
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)   # Start
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
AQUA = (0, 255, 255)     # Closed
INDIGO = (63, 0, 255)    # Open
GOLD = (255, 215, 0)     # Path

ROWS = 30
algorithm_selected = ['DFS']

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = BLACK
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == AQUA

    def is_open(self):
        return self.color == INDIGO

    def is_barrier(self):
        return self.color == WHITE

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = AQUA

    def make_open(self):
        self.color = INDIGO

    def make_barrier(self):
        self.color = WHITE

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = GOLD

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])  # Down
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])  # Up
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])  # Right
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])  # Left

def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def dfs(draw, grid, start, end):
    stack = [start]
    came_from = {}
    visited = set()

    while stack:
        current = stack.pop()
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        if current not in visited:
            visited.add(current)
            current.make_closed()
            for neighbour in current.neighbours:
                if neighbour not in visited and not neighbour.is_barrier():
                    came_from[neighbour] = current
                    stack.append(neighbour)
                    neighbour.make_open()
        draw()
    return False

def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        current = queue.get()
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbour in current.neighbours:
            if neighbour not in visited and not neighbour.is_barrier():
                visited.add(neighbour)
                came_from[neighbour] = current
                queue.put(neighbour)
                neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    dist = {spot: float("inf") for row in grid for spot in row}
    dist[start] = 0
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            temp_dist = dist[current] + 1
            if temp_dist < dist[neighbour]:
                dist[neighbour] = temp_dist
                came_from[neighbour] = current
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((dist[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g
                f_score[neighbour] = temp_g + h_score(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x,y = pos
    row = y // gap
    col = x // gap
    return row, col

def main_algorithm():
    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None
    run = True
    started = False

    def redraw(): draw(WIN, grid, ROWS, WIDTH)

    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    if algorithm_selected[0] == 'DFS':
                        dfs(redraw, grid, start, end)
                    elif algorithm_selected[0] == 'BFS':
                        bfs(redraw, grid, start, end)
                    elif algorithm_selected[0] == 'Dijkstra':
                        dijkstra(redraw, grid, start, end)
                    elif algorithm_selected[0] == 'Astar':
                        astar(redraw, grid, start, end)

                if event.key == pygame.K_c:
                    grid = make_grid(ROWS, WIDTH)
                    start = None
                    end = None

def set_algorithm(value, algo):
    algorithm_selected[0] = algo

def home():
    menu = pygame_menu.Menu('THE PATHFINDER', WIDTH, WIDTH, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label('THE PATHFINDER', font_size=50)
    menu.add.selector('Algorithm: ', [('DFS', 'DFS'), ('BFS', 'BFS'), ('Dijkstra', 'Dijkstra'), ('Astar', 'Astar')], onchange=set_algorithm)
    menu.add.button('PLAY', main_algorithm)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        WIN.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(WIN)
        pygame.display.update()


home()


# A star search path finding algorithm using pygame as a library for creating a visual app

# STEPS

# 1. Create a class that represents a node with parameters of its neighboring node as cubes
# 2. Create a function that draws a 2x2 grid with a 600 x 600 width by width using pygame library built-in function 
# 3. Implement the A star search path finding algorithm 
# 4. Create a function that will backtrack its way after finding the best path to the goal
# 5. Lastly, create the main function by combining all the previous functions, then create a while loop
#  It will run until the user exits the app.



import pygame #import pygame library 
import math 
from queue import PriorityQueue 

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A star Path Finding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == WHITE

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = WHITE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid): # check down, up, right and left 
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])



    def __lt__(self, other):
        return False


def h(p1, p2): #h score or estimate distance from the current node to the goal
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw): #backtrack
    while current in came_from: # if the current node is in the came_from set
        current = came_from[current]
        current.make_path() #draw the path where we came 
        draw()

def algorithm(draw, grid, start, end): # A star search algorithm
    count = 0
    open_set = PriorityQueue() # minimum value 
    open_set.put((0, count, start)) # put f(n) or f score in the open set (f(n), count, spot or node)
    came_from = {} # keeps track of the last node it came from
    g_score = {spot: float("inf") for row in grid for spot in row} #float infinity 
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) #heuristic 

    open_set_hash = {start} #set of node

    while not open_set.empty(): #initialize 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit the while loop
                pygame.quit()

        current = open_set.get()[2] # indexing the node
        open_set_hash.remove(current) #remove the node from the hash

        if current == end: # if true we found the path
            reconstruct_path(came_from, end, draw)
            end.make_end()
             # make path 
            return True 
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # distance of every node to the next is 1

            if temp_g_score < g_score[neighbor]: # if the temp g(n) is better the other node, update
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) # f(n) = g(n) + h(n)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start: # if the node that is considered is not the start node
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
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

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row,col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # mouse left click
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_start()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # mouse right click
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
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
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()

main(WIN, WIDTH)







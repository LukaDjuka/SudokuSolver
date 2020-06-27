"""
The GUI for the SudokuSolver

********************************************************************************
*** NOT MY CODE ***
*** ALL CODE CURRENTLY USED IN THIS MODULE IS FROM:
http://trevorappleton.blogspot.com/2013/10/guide-to-creating-sudoku-solver-using.html

WILL IMPLEMENT PERSONAL ADDITIONS TO THIS CODE AT A LATER DATE
THE CODE IN SudokuSolver.py IS MY OWN CODE.
ITS IMPLEMENTATION INTO THIS GUI IS A PERSONAL ADDITION.

************************************************************************************
ATTEMPTS to:
Uses pygame as the basis for the GUI and allows the user to:
    - Input values in the unit squares
    - Erase values in the unit squares
    - Input temporary values in the unit squares (they hover in the top right corner)
    - See final answer and realtime process of how it is found

    - *** Compare user input to final answer key ***

By: Luka Djukic
"""
import pygame, sys
from pygame.locals import *
import SudokuSolver as Sudoku

WINDOWMULTIPLIER = 5    # Modify this number to change the size of the grid
WINDOWSIZE = 81
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = (WINDOWSIZE * WINDOWMULTIPLIER) // 3
CELLSIZE = SQUARESIZE // 3
NUMBERSIZE = CELLSIZE // 3


BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

FPS = 10

def draw_grid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

    for x in range(0, WINDOWWIDTH, SQUARESIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, SQUARESIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))
    return None

def initiate_cells():
    current_grid = {}
    full_cell = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for x_coordinate in range(9):
        for y_coordinate in range(9):
            current_grid[x_coordinate, y_coordinate] = list(full_cell)
    return current_grid

def display_cells(current_grid: dict):
    x_factor = 0
    y_factor = 0
    for item in current_grid:
        cell_data = current_grid[item]
        for number in cell_data:
            if number != ' ':
                x_factor = ((number - 1) % 3)
                if number <= 3:
                    y_factor = 0
                elif number <= 6:
                    y_factor = 1
                else:
                    y_factor = 2
                if cell_data.count(' ') < 8:
                    populate_cells(number, (item[0] * CELLSIZE) + (x_factor * NUMBERSIZE),
                                   (item[1] * CELLSIZE) + (y_factor * NUMBERSIZE), 'small')
                else:
                    populate_cells(number, (item[0] * CELLSIZE), (item[1] * CELLSIZE), 'large')
    return None

def populate_cells(cell_data: int, x, y, size):
    if size == 'small':
        cell_surf = BASICFONT.render('%s' %(cell_data), True, GRAY)
    elif size == 'large':
        cell_surf = LARGEFONT.render('%s' % (cell_data), True, GREEN)
    cell_rect = cell_surf.get_rect()
    cell_rect.topleft = (x, y)
    DISPLAYSURF.blit(cell_surf, cell_rect)

def draw_box(mouse_x, mouse_y):
    box_x = ((mouse_x * 27) / WINDOWWIDTH) * (NUMBERSIZE)
    box_y = ((mouse_y * 27) / WINDOWHEIGHT) * (NUMBERSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, (box_x, box_y, NUMBERSIZE, NUMBERSIZE), 1)

def display_selected_number(mouse_x, mouse_y, current_grid):
    x_num = (mouse_x * 27) // WINDOWWIDTH
    y_num = (mouse_y * 27) // WINDOWWIDTH

    mod_x_num = x_num % 3
    mod_y_num = y_num % 3

    if mod_x_num == 0:
        x_choices = [1, 4, 7]
        number = x_choices[mod_y_num]
    elif mod_x_num == 1:
        x_choices = [2, 5, 8]
        number = x_choices[mod_y_num]
    else:
        x_choices = [3, 6, 9]
        number = x_choices[mod_y_num]
    x_cell_num = x_num // 3
    y_cell_num = y_num // 3

    current_state = current_grid[x_cell_num, y_cell_num]
    inc_num = 0

    while inc_num < 9:
        if (inc_num + 1) != number:
            current_state[inc_num] = ' '
        else:
            current_state[inc_num] = number
        current_grid[x_cell_num, y_cell_num] = current_state
        inc_num += 1
    return current_grid

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BASICFONTSIZE, LARGEFONT, LARGEFONTSIZE
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(WHITE)
    mouse_clicked = False
    mouse_x = 0
    mouse_y = 0
    BASICFONTSIZE = 15
    LARGEFONTSIZE = 55
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    LARGEFONT = pygame.font.Font('freesansbold.ttf', LARGEFONTSIZE)
    current_grid = initiate_cells()
    display_cells(current_grid)
    draw_grid()
    pygame.display.set_caption('Sudoku Solver')

    while True:
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True
        if mouse_clicked:
            current_grid = display_selected_number(mouse_x, mouse_y, current_grid)

        DISPLAYSURF.fill(WHITE)
        display_cells(current_grid)
        draw_grid()
        draw_box(mouse_x, mouse_y)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()

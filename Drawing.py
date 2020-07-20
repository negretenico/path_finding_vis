from Colors import Color
from Spot import Spot
import pygame
class Draw:
    def __init__(self):
        self.color = Color()
        self.WIDTH = 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        pygame.display.set_caption("A* Path Finding Algorithm")



    def make_grid(self,rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)

        return grid

    def draw_grid(self,win, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, self.color.GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, self.color.GREY, (j * gap, 0), (j * gap, width))

    def draw(self,win, grid, rows, width):
        win.fill(self.color.WHITE)
        for row in grid:
            for spot in row:
                spot.draw(win)
                if(spot.y ==0 or spot.x == 0 or spot.x == win.get_width()-spot.width or spot.y == win.get_height()-spot.width):
                    spot.make_barrier()
        self.draw_grid(win, rows, width)
        pygame.display.update()



    def get_clicked_pos(self,pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

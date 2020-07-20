from Spot import Spot
from Drawing import Draw
import pygame
from heapq import heappush, heappop
import math
import tkinter as tk
class Algorithm:
    def __init__(self):
        self.draw_obj = Draw()
        self.name = ""
    def reconstruct_path(self,came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()
    def a_star(self,draw,grid, start, end):
        dist = self.heuristic(start, end)
        openset = []
        heappush(openset, (0, start))
        closedset = set()
        parents = {}
        costs = {}

        while len(openset) > 0:
            draw()
            start.make_start()
            currentCost, state = heappop(openset)
            currentCost = currentCost - self.heuristic(state, end)
            if state.is_end():
                print("Found goal!")
                # retrieve series of steps that brought us here (use the parents map)
                self.reconstruct_path(parents, end, draw)
                end.make_end()
                start.make_start()
                return True
            else:
                if not state in closedset:
                    for neighbor in state.neighbors:
                        f = currentCost + self.heuristic(neighbor, end)
                        heappush(openset, (f, neighbor))
                        if neighbor not in closedset:
                            end.make_end()
                            if neighbor not in parents:
                                parents[neighbor] = state
                                costs[neighbor] = f
                                neighbor.make_open()
                            elif f < costs[neighbor]:
                                costs[neighbor] = f
                                parents[neighbor] = state
                                neighbor.make_open()
                    state.make_closed()
                    closedset.add(state)

    def depth_first(self,draw,grid, start, end):
        closedset = []
        openset = [start]  # openset starts with starting state
        parents = {}
        while len(openset) > 0:
            state = openset.pop()  # get most-recently-added element from openset'
            #   # ...
            if (state.is_end()):
                print("Found goal!")
                # retrieve series of steps that brought us here (use the parents map)
                self.reconstruct_path(parents, end, draw)
                start.make_start()
                end.make_end()
                return True
            else:
                state.make_closed()
                for neighbor in state.neighbors:
                    draw()
                    if (neighbor not in closedset):
                        neighbor.make_open()
                        end.make_end()
                        openset.append(neighbor)
                        closedset.append(state)
                        parents[neighbor] = state



    def bredth_first(self,draw,grid, start, end):
        openset = [start]
        closedset = set()
        parents = {}
        while (len(openset) > 0):
            state = openset.pop(0)
            if (state.is_end()):
                print("Found goal!")
                # retrieve series of steps that brought us here (use the parents map)
                self.reconstruct_path(parents, end, draw)
                start.make_start()
                end.make_end()
                return True
            else:
                if not state in closedset:
                    state.make_closed()
                    for neighbor in state.neighbors:
                        draw()
                        #       # next_state is something like (4, 2) (coordinates)
                        #       # action is something like WEST
                        #       # cost is not used for depthd-fir
                        if neighbor not in closedset:
                            openset.append(neighbor)
                            neighbor.make_open()
                            end.make_end()
                            if not neighbor in parents:
                                parents[neighbor] = state
                    closedset.add(state)



    def heuristic(self,p1,p2):
        x1, y1 = p1.x,p1.y
        x2, y2 = p2.x,p2.y
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    def choice(self):
        window = tk.Tk()

        window.title("Python Tkinter Text Box")
        window.minsize(200, 200)

        def clickMe():
            window.destroy()
            self.name = name.get()

        label = tk.Label(window, text="Enter Your Name")
        label.grid(column=0, row=0)
        label = tk.Label(window, text="Enter Algorithm")
        label.grid(column=0, row=0)

        name = tk.StringVar()
        nameEntered = tk.Entry(window, width=15, textvariable=name)

        nameEntered.grid(column=0, row=1)

        button = tk.Button(window, text="Click Me", command=clickMe)
        button.grid(column=0, row=2)

        window.mainloop()

    def main(self):
        draw_obj = Draw()
        ROWS = 50
        grid = draw_obj.make_grid(ROWS, draw_obj.WIDTH)
        start = None
        end = None

        run = True
        self.choice()
        while run:
            draw_obj.draw(draw_obj.WIN, grid, ROWS, draw_obj.WIDTH)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = draw_obj.get_clicked_pos(pos, ROWS, draw_obj.WIDTH)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = draw_obj.get_clicked_pos(pos, ROWS, draw_obj.WIDTH)
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

                        if self.name.upper() == 'A STAR':
                            self.a_star(lambda: draw_obj.draw(draw_obj.WIN, grid, ROWS, draw_obj.WIDTH), grid, start, end)
                        elif self.name.upper() =='DFS':
                            self.depth_first(lambda: draw_obj.draw(draw_obj.WIN, grid, ROWS, draw_obj.WIDTH), grid, start, end)
                        elif self.name.upper() =='BFS':
                            self.bredth_first(lambda: draw_obj.draw(draw_obj.WIN, grid, ROWS, draw_obj.WIDTH), grid, start, end)


                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = draw_obj.make_grid(ROWS, draw_obj.WIDTH)

        pygame.quit()


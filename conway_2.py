
from collections import defaultdict

import pygame
import sys




if __name__ == "__main__":

    try:

        class GameOfLife:

            def __init__(self):
                
                pygame.init()

                self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT = 1280, 720
                self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

                self.FPS = 60

                self.CLOCK = pygame.time.Clock()

                self.CELL_SIZE = 10
                self.GRID_WIDTH, self.GRID_HEIGHT = self.DISPLAY_WIDTH // self.CELL_SIZE, self.DISPLAY_HEIGHT // self.CELL_SIZE

                self.NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1),
                                  ( 0, -1),          ( 0, 1),
                                  ( 1, -1), ( 1, 0), ( 1, 1)]


                self.mouse_cell_surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(self.mouse_cell_surface, (255, 255, 255, 50), (0, 0, self.CELL_SIZE, self.CELL_SIZE))                


                self.paused = True
                self.generation_step_rate = 0.0

                self.last_time_step = pygame.time.get_ticks()

                self.live_cells = {(2, 0), (3, 1), (3, 2), (2, 2), (1, 2)}



            def step_generation(self):

                neighbor_counts = defaultdict(int)

                for (x, y) in self.live_cells:
                    for dx, dy in self.NEIGHBORS:
                        neighbor_counts[(x + dx, y + dy)] += 1
                
                new_live_cells = set()
                for cell, count in neighbor_counts.items():
                    if count == 3 or (count == 2 and cell in self.live_cells):
                        new_live_cells.add(cell)
                
                self.live_cells = new_live_cells



            def render_grid(self):
                
                for (x, y) in self.live_cells:
                    px = x * self.CELL_SIZE
                    py = y * self.CELL_SIZE
                    pygame.draw.rect(self.DISPLAY, (255, 255, 255), (px, py, self.CELL_SIZE, self.CELL_SIZE))

            

            def quit_game(self):

                pygame.quit()
                sys.exit()

            

            def reset(self):

                self.live_cells = set()

            

            def update_grid(self):

                if 0 <= pygame.mouse.get_pos()[0] <= self.DISPLAY_WIDTH and 0 <= pygame.mouse.get_pos()[1] <= self.DISPLAY_HEIGHT:

                    snap_x = (pygame.mouse.get_pos()[0] // self.CELL_SIZE) * self.CELL_SIZE
                    snap_y = (pygame.mouse.get_pos()[1] // self.CELL_SIZE) * self.CELL_SIZE
                    self.DISPLAY.blit(self.mouse_cell_surface, (snap_x, snap_y))

                    absolute_pos = (snap_x // self.CELL_SIZE, snap_y // self.CELL_SIZE)

                    if pygame.mouse.get_pressed()[0] and absolute_pos not in self.live_cells:
                        self.live_cells.add(absolute_pos)
                    if pygame.mouse.get_pressed()[2] and absolute_pos in self.live_cells:
                        self.live_cells.remove(absolute_pos)



            def handle_input_event(self):

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                    if event.type == pygame.MOUSEWHEEL:
                        self.generation_step_rate -= event.y * 0.05
                        self.generation_step_rate = round(max(0.0, min(self.generation_step_rate, 1.0)), 2)

                
                just_pressed = pygame.key.get_just_pressed()
                if just_pressed[pygame.K_ESCAPE]:
                    self.quit_game()
                if just_pressed[pygame.K_SPACE]:
                    self.paused = not self.paused
                if just_pressed[pygame.K_BACKSPACE]:
                    self.reset()



            def mainloop(self):

                while True:

                    self.DISPLAY.fill((10, 10, 10))
                    self.render_grid()

                    now = pygame.time.get_ticks()

                    if self.paused:
                        self.update_grid()
                    else:
                        if now - self.last_time_step >= self.generation_step_rate * 1000:
                            self.step_generation()
                            self.last_time_step = now
                        

                    self.handle_input_event()

                    pygame.display.update()
                    self.CLOCK.tick(self.FPS)
            
        

        GameOfLife().mainloop()



    except Exception as e:
        raise e

from dataclasses import dataclass

import sys

import pygame





class GameOfLife:

    def __init__(self):
        
        pygame.init()

        self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT = 1280, 720

        self.CELL_SIZE = 10
        self.GRID_WIDTH, self.GRID_HEIGHT = self.DISPLAY_WIDTH // self.CELL_SIZE, self.DISPLAY_HEIGHT // self.CELL_SIZE
        

        self.FPS = 60


        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()


        self.mouse_cell_surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.mouse_cell_surface, (255, 255, 255, 50), (0, 0, self.CELL_SIZE, self.CELL_SIZE))
        

        self.paused = True
        self.gen_speed = 0.5

        self.last_step_time = pygame.time.get_ticks()


        @dataclass
        class Cell:
            nc: int = 0
            state: bool = False

        self.grid = [[Cell() for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]



    def quit_game(self):

        pygame.quit()
        sys.exit()



    def handle_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            elif event.type == pygame.MOUSEWHEEL:
                    self.gen_speed -= event.y * 0.1
                    self.gen_speed = round(max(0.0, min(self.gen_speed, 1.0)), 1)
            
        just_pressed = pygame.key.get_just_pressed()
        if just_pressed[pygame.K_ESCAPE]:
            self.quit_game()
        if just_pressed[pygame.K_SPACE]:
            self.paused = not self.paused
        if just_pressed[pygame.K_BACKSPACE]:
            self.clear_grid()
    


    def render_grid(self):
        
        for row in range(self.GRID_HEIGHT):
            for cell in range(self.GRID_WIDTH):
                if self.grid[row][cell].state:
                    rect = pygame.Rect(cell * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    pygame.draw.rect(self.DISPLAY, (255, 255, 255), rect)




    def step_generation(self):
        

        for row in range(self.GRID_HEIGHT):
            for cell in range(self.GRID_WIDTH):
                
                try:
                    if self.grid[row][cell].state:

                        self.grid[row-1][cell-1].nc += 1    # top left
                        self.grid[row-1][cell].nc += 1      # top
                        self.grid[row-1][cell+1].nc += 1    # top right

                        self.grid[row][cell-1].nc += 1      # left
                        self.grid[row][cell+1].nc += 1      # right

                        self.grid[row+1][cell-1].nc += 1    # bottom left
                        self.grid[row+1][cell].nc += 1      # bottom
                        self.grid[row+1][cell+1].nc += 1    # bottom right

                except IndexError:
                    pass

        
        for row in self.grid:
            for cell in row:
                
                if cell.nc < 2 or cell.nc > 3:
                    cell.state = False

                if not cell.state and cell.nc == 3:
                    cell.state = True
                
                cell.nc = 0



    def mouse_cursor_updates(self):

        if 0 <= pygame.mouse.get_pos()[0] <= self.DISPLAY_WIDTH and 0 <= pygame.mouse.get_pos()[1] <= self.DISPLAY_HEIGHT:

            snap_x = (pygame.mouse.get_pos()[0] // self.CELL_SIZE) * self.CELL_SIZE
            snap_y = (pygame.mouse.get_pos()[1] // self.CELL_SIZE) * self.CELL_SIZE
            self.DISPLAY.blit(self.mouse_cell_surface, (snap_x, snap_y))

            try:
                if self.paused and pygame.mouse.get_pressed()[0]:
                    self.grid[snap_y // self.CELL_SIZE][snap_x // self.CELL_SIZE].state = True
                elif self.paused and pygame.mouse.get_pressed()[2]:
                    self.grid[snap_y // self.CELL_SIZE][snap_x // self.CELL_SIZE].state = False
            
            except IndexError:
                pass
    


    def clear_grid(self):

        for row in self.grid:
            for cell in row:
                cell.state = False



    def main_loop(self):

        while True:
                
            self.DISPLAY.fill((10, 10, 10))

            now = pygame.time.get_ticks()
            if self.paused:
                self.mouse_cursor_updates()
            else:
                if now - self.last_step_time >= self.gen_speed * 1000:
                    self.step_generation()
                    self.last_step_time = now

            
            self.render_grid()
            self.handle_event()

            pygame.display.flip()
            self.CLOCK.tick(self.FPS)
    


    def start_screen(self):

        # Screen text for controls and crap too lazy rn tho

        # space to pause and unpause
        # back space to clear grid
        # scroll to change the generation time delay
        # escape to quit
        # left click to place, right click to delete

        self.main_loop()





if __name__ == "__main__":

    g = GameOfLife()
    g.start_screen()


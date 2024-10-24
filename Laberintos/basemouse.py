import pygame

class BaseMouse:
    def __init__(self, maze, start_x, start_y):
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.direction = 'E'  # El ratón empieza dirigiéndose al Este (derecha)
        self.directions = ['E', 'S', 'W', 'N']  # Dirección en el sentido de las agujas del reloj
        self.movements = 0  # Contador de movimientos
        self.cell_visits = 0  # Contador de visitas a celdas
        self.visited_cells = set()  # Para asegurar que las visitas no se dupliquen

    def move(self):
        raise NotImplementedError("Este método debe ser implementado por la clase hija")

    def move_forward(self):
        if self.direction == 'E':
            self.x += 1
        elif self.direction == 'N':
            self.y -= 1
        elif self.direction == 'W':
            self.x -= 1
        elif self.direction == 'S':
            self.y += 1

    def can_move_forward(self):
        if self.direction == 'E' and not self.maze[self.y][self.x].east:
            return True
        elif self.direction == 'N' and not self.maze[self.y][self.x].north:
            return True
        elif self.direction == 'W' and not self.maze[self.y][self.x].west:
            return True
        elif self.direction == 'S' and not self.maze[self.y][self.x].south:
            return True
        return False

    def can_move_right(self):
        if self.direction == 'E' and not self.maze[self.y][self.x].south:
            return True
        elif self.direction == 'S' and not self.maze[self.y][self.x].west:
            return True
        elif self.direction == 'W' and not self.maze[self.y][self.x].north:
            return True
        elif self.direction == 'N' and not self.maze[self.y][self.x].east:
            return True
        return False

    def record_visit(self):
        current_cell = (self.x, self.y)
        if current_cell not in self.visited_cells:
            self.cell_visits += 1
            self.visited_cells.add(current_cell)

    def turn_right(self):
        idx = self.directions.index(self.direction)
        self.direction = self.directions[(idx + 1) % 4]

    def turn_left(self):
        idx = self.directions.index(self.direction)
        self.direction = self.directions[(idx - 1) % 4]

    def check_exit(self, exit_x, exit_y):
        return self.x == exit_x and self.y == exit_y

    def draw(self, screen, pixel_size):
        pygame.draw.ellipse(screen, (255, 0, 0),
                            (self.x * pixel_size + pixel_size // 4,
                             self.y * pixel_size + pixel_size // 4,
                             pixel_size // 2, pixel_size // 2))
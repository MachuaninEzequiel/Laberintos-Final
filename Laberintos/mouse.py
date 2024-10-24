import pygame


class Mouse:
    def __init__(self, maze, start_x, start_y):
        self.name = 'Mouse Derecha'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.direction = 'E'  # El ratón empieza dirigiéndose al Este (derecha)
        self.directions = ['E', 'S', 'W', 'N']  # Dirección en el sentido de las agujas del reloj
        self.movements = 0  # Contador de movimientos
        self.cell_visits = 0  # Contador de visitas a celdas
        self.visited_cells = set()  # Para asegurar que las visitas no se dupliquen
        self.speed = 1
        self.boost_duration = 0  # Duración del boost en frames
        self.original_speed = 1
        self.boost_count = 0
        self.calculation_count = 0

    def move(self):
        # Verificar si el boost está activo
        if self.boost_duration > 0:
            self.boost_duration -= 1
            if self.boost_duration == 0:
                self.speed = self.original_speed

        # Seguir la pared a la derecha
        if self.can_move_right():
            self.turn_right()
            self.move_forward()
        elif self.can_move_forward():
            self.move_forward()
        else:
            self.turn_left()
        # Incrementar movimientos
        self.movements += 1
        # Registrar la visita a la nueva celda
        self.record_visit()
        

    def move_forward(self):
        # Moverse en la dirección actual
        if self.direction == 'E':
            self.x += 1
        elif self.direction == 'N':
            self.y -= 1
        elif self.direction == 'W':
            self.x -= 1
        elif self.direction == 'S':
            self.y += 1

    def can_move_forward(self):
        # Verifica si puede moverse en la dirección actual
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
        # Verifica si puede moverse a la derecha en función de la dirección actual
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
        # Solo registrar si es la primera vez que se visita esta celda
        if current_cell not in self.visited_cells:
            self.cell_visits += 1
            self.visited_cells.add(current_cell)
    
    
    def turn_right(self):
        # Cambiar la dirección en el sentido de las agujas del reloj
        idx = self.directions.index(self.direction)
        self.direction = self.directions[(idx + 1) % 4]

    def turn_left(self):
        # Cambiar la dirección en el sentido contrario a las agujas del reloj
        idx = self.directions.index(self.direction)
        self.direction = self.directions[(idx - 1) % 4]

    def check_exit(self, exit_x, exit_y):
        # Verificamos si el ratón ha llegado a la salida
        return self.x == exit_x and self.y == exit_y
    
    def speed_boost(self):
        self.boost_duration = 600  # Duración del boost en frames (10 segundos a 60 FPS)
        self.speed = self.original_speed * 2
        self.boost_count += 1


    def draw(self, screen, pixel_size):
        # Dibujar el ratón en rojo
        pygame.draw.ellipse(screen, (255, 0, 0),
                            (self.x * pixel_size + pixel_size // 4,
                             self.y * pixel_size + pixel_size // 4,
                             pixel_size // 2, pixel_size // 2))
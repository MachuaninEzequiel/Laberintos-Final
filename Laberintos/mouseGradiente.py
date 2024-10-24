import pygame
import math


class MouseGradiente:
    def __init__(self, maze, start_x, start_y, exit_x, exit_y):
        self.name = 'Mouse Gradiente'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.exit_x = exit_x
        self.exit_y = exit_y
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

        # Elegir la dirección basada en el gradiente
        best_direction = self.get_best_direction()

        if best_direction == 'E':
            self.x += 1
        elif best_direction == 'N':
            self.y -= 1
        elif best_direction == 'W':
            self.x -= 1
        elif best_direction == 'S':
            self.y += 1

        # Incrementar movimientos
        self.movements += 1
        # Registrar la visita a la nueva celda
        self.record_visit()

    def get_best_direction(self):
        # Calcular las distancias a la salida para cada dirección posible
        distances = {}
        if not self.maze[self.y][self.x].east:
            distances['E'] = self.calculate_distance(self.x + 1, self.y)
        if not self.maze[self.y][self.x].west:
            distances['W'] = self.calculate_distance(self.x - 1, self.y)
        if not self.maze[self.y][self.x].north:
            distances['N'] = self.calculate_distance(self.x, self.y - 1)
        if not self.maze[self.y][self.x].south:
            distances['S'] = self.calculate_distance(self.x, self.y + 1)

        # Devolver la dirección con la menor distancia
        if distances:
            return min(distances, key=distances.get)
        else:
            return None

    def calculate_distance(self, x, y):
        # Calcular la distancia euclidiana al objetivo (salida)
        return math.sqrt((x - self.exit_x) ** 2 + (y - self.exit_y) ** 2)

    def record_visit(self):
        current_cell = (self.x, self.y)
        # Solo registrar si es la primera vez que se visita esta celda
        if current_cell not in self.visited_cells:
            self.cell_visits += 1
            self.visited_cells.add(current_cell)

    def check_exit(self):
        # Verificamos si el ratón ha llegado a la salida
        return self.x == self.exit_x and self.y == self.exit_y

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
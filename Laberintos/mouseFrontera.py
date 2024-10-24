import pygame
from collections import deque

class MouseFrontera:
    def __init__(self, maze, start_x, start_y):
        self.name = 'Mouse Búsqueda de Frontera'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.movements = 0  # Contador de movimientos
        self.cell_visits = 0  # Contador de visitas a celdas
        self.visited_cells = set()  # Para asegurar que las visitas no se dupliquen
        self.frontier = deque()  # Cola para la frontera de celdas no exploradas
        self.frontier.append((start_x, start_y))  # Inicialmente, la frontera contiene solo la celda inicial
        self.direction = None  # No usaremos una dirección fija en esta exploración
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

        # Si la frontera está vacía, el ratón ha explorado todo lo posible
        if not self.frontier:
            return
        
        # Sacar la primera celda de la frontera
        next_cell = self.frontier.popleft()
        self.x, self.y = next_cell
        
        # Registrar la visita a la nueva celda
        self.record_visit()
        
        # Añadir las celdas no visitadas adyacentes a la frontera
        self.add_frontier_cells()
        
        # Incrementar movimientos
        self.movements += 1

    def add_frontier_cells(self):
        # Añadir las celdas no visitadas adyacentes a la frontera
        neighbors = self.get_neighbors(self.x, self.y)
        for neighbor in neighbors:
            if neighbor not in self.visited_cells and neighbor not in self.frontier:
                self.frontier.append(neighbor)

    def get_neighbors(self, x, y):
        # Obtener las celdas vecinas en función de la estructura del laberinto
        neighbors = []
        if y > 0 and not self.maze[y][x].north:  # Norte
            neighbors.append((x, y - 1))
        if y < len(self.maze) - 1 and not self.maze[y][x].south:  # Sur
            neighbors.append((x, y + 1))
        if x > 0 and not self.maze[y][x].west:  # Oeste
            neighbors.append((x - 1, y))
        if x < len(self.maze[0]) - 1 and not self.maze[y][x].east:  # Este
            neighbors.append((x + 1, y))
        return neighbors

    def record_visit(self):
        current_cell = (self.x, self.y)
        # Solo registrar si es la primera vez que se visita esta celda
        if current_cell not in self.visited_cells:
            self.cell_visits += 1
            self.visited_cells.add(current_cell)
    
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
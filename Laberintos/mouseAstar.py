import pygame
import heapq

class AStarMouse:
    def __init__(self, maze, start_x, start_y, exit_x, exit_y):
        self.name = 'Mouse ColapinA*'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.exit_x = exit_x  # Coordenada de salida
        self.exit_y = exit_y  # Coordenada de salida
        self.movements = 0  # Contador de movimientos
        self.cell_visits = 0  # Contador de visitas a celdas
        self.visited_cells = set()  # Para asegurar que las visitas no se dupliquen
        self.path = []  # Almacena el camino encontrado por A*
        self.speed = 1
        self.boost_duration = 0  # Duración del boost en frames
        self.original_speed = 1
        self.boost_count = 0
        self.calculation_count = 0  # Contador de celdas procesadas

    def move(self):
        # Verificar si el boost está activo
        if self.boost_duration > 0:
            self.boost_duration -= 1
            if self.boost_duration == 0:
                self.speed = self.original_speed

        # Si hay un camino predefinido, seguirlo
        if self.path:
            next_cell = self.path.pop(0)
            self.x, self.y = next_cell
            self.movements += 1
            self.record_visit()
        else:
            self.find_path()  # Busca un nuevo camino si no hay

    def find_path(self):
        # Implementación del algoritmo A*
        start = (self.x, self.y)
        goal = (self.exit_x, self.exit_y)

        # Verificar que exit_x y exit_y no sean None
        if self.exit_x is None or self.exit_y is None:
            print("Error: Las coordenadas de salida no están definidas.")
            return

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            # Contar la celda procesada
            self.calculation_count += 1

            if current == goal:
                self.reconstruct_path(came_from, current)
                return

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1  # Suponiendo que cada movimiento cuesta 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    def heuristic(self, a, b):
        # Heurística de distancia Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        self.path = total_path[1:]  # Excluye la celda de inicio

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell

        # Verifica las celdas adyacentes
        if x + 1 < len(self.maze[0]) and not self.maze[y][x].east:  # Este
            neighbors.append((x + 1, y))
        if x - 1 >= 0 and not self.maze[y][x].west:  # Oeste
            neighbors.append((x - 1, y))
        if y - 1 >= 0 and not self.maze[y][x].north:  # Norte
            neighbors.append((x, y - 1))
        if y + 1 < len(self.maze) and not self.maze[y][x].south:  # Sur
            neighbors.append((x, y + 1))

        return neighbors

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
        # Dibujar el ratón en azul
        pygame.draw.ellipse(screen, (0, 0, 255),
                            (self.x * pixel_size + pixel_size // 4,
                             self.y * pixel_size + pixel_size // 4,
                             pixel_size // 2, pixel_size // 2))
import pygame

class MaximumFlowMouse:
    def __init__(self, maze, start_x, start_y, exit_x, exit_y):
        self.name = 'Mouse MaximumFlow'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.exit_x = exit_x  # Coordenada de salida
        self.exit_y = exit_y  # Coordenada de salida
        self.movements = 0  # Contador de movimientos
        self.cell_visits = 0  # Contador de visitas a celdas
        self.visited_cells = set()  # Para asegurar que las visitas no se dupliquen
        self.path = []  # Almacena el camino encontrado por Maximum Flow
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
        # Implementación del algoritmo de flujo máximo (usando BFS como ejemplo)
        start = (self.x, self.y)
        goal = (self.exit_x, self.exit_y)

        # Verificar que las coordenadas de salida no sean None
        if self.exit_x is None or self.exit_y is None:
            print("Error: Las coordenadas de salida no están definidas.")
            return

        # Aquí se busca el flujo máximo entre las celdas
        self.path = self.bfs_maximum_flow(start, goal)

    def bfs_maximum_flow(self, source, sink):
        # Implementación simplificada del algoritmo de flujo máximo usando BFS
        visited = set()
        queue = [(source, [source])]

        while queue:
            current, path = queue.pop(0)
            self.calculation_count += 1  # Contar la celda procesada

            if current == sink:
                return path[1:]  # Excluye la celda de inicio

            if current not in visited:
                visited.add(current)
                for neighbor in self.get_neighbors(current):
                    if neighbor not in visited:  # Verificar si ya ha sido visitado
                        queue.append((neighbor, path + [neighbor]))
        return []  # Retorna vacío si no hay un camino

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell

        # Verifica las celdas adyacentes y comprueba si hay paredes
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
        # Placeholder para dibujar el ratón
        pygame.draw.ellipse(screen, (0, 0, 255),
                            (self.x * pixel_size + pixel_size // 4,
                             self.y * pixel_size + pixel_size // 4,
                             pixel_size // 2, pixel_size // 2))

import pygame
import heapq
import math

class MousePonderado:
    def __init__(self, maze, start_x, start_y, exit_x, exit_y):
        self.name = 'Mouse Heurístico Ponderado'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.weight = 1.0
        self.movements = 0
        self.cell_visits = 0
        self.visited_cells = set()
        self.speed = 1
        self.boost_duration = 0
        self.original_speed = 1
        self.boost_count = 0
        self.calculation_count = 0
        self.directions = ['E', 'S', 'W', 'N']  # Direcciones cardinales
        self.direction_vectors = {'E': (1, 0), 'S': (0, 1), 'W': (-1, 0), 'N': (0, -1)}  # Vectores de movimiento

    def move(self):
        # Verificar si el boost está activo
        if self.boost_duration > 0:
            self.boost_duration -= 1
            if self.boost_duration == 0:
                self.speed = self.original_speed

        # Usar búsqueda heurística ponderada para decidir el siguiente movimiento
        next_move = self.heuristic_weighted_search()
        if next_move:
            self.x, self.y = next_move
            self.movements += 1
            self.record_visit()

    def heuristic_weighted_search(self):
        # Implementación básica de búsqueda ponderada
        # Utiliza una cola de prioridad (min heap) para almacenar las celdas según la función f(n) = g(n) + weight * h(n)
        frontier = []
        heapq.heappush(frontier, (0, (self.x, self.y)))  # Inicia en la posición actual

        # Usar un diccionario para almacenar el costo mínimo hasta el momento
        cost_so_far = { (self.x, self.y): 0 }
        came_from = { (self.x, self.y): None }

        while frontier:
            _, current = heapq.heappop(frontier)
            cur_x, cur_y = current

            # Verificar si llegamos a la salida
            if (cur_x, cur_y) == (self.exit_x, self.exit_y):
                return self.reconstruct_path(came_from, current)

            # Explorar vecinos
            for direction in self.directions:
                dx, dy = self.direction_vectors[direction]
                next_x, next_y = cur_x + dx, cur_y + dy

                if self.is_valid_move(next_x, next_y):
                    new_cost = cost_so_far[(cur_x, cur_y)] + 1  # Suponiendo que cada movimiento cuesta 1

                    if (next_x, next_y) not in cost_so_far or new_cost < cost_so_far[(next_x, next_y)]:
                        cost_so_far[(next_x, next_y)] = new_cost
                        priority = new_cost + self.weight * self.heuristic(next_x, next_y)
                        heapq.heappush(frontier, (priority, (next_x, next_y)))
                        came_from[(next_x, next_y)] = current

        return None  # Si no hay más movimientos válidos

    def heuristic(self, x, y):
        # Calcular la distancia heurística (por ejemplo, Manhattan) entre la posición actual y la salida
        return abs(x - self.exit_x) + abs(y - self.exit_y)

    def reconstruct_path(self, came_from, current):
        # Reconstruir el camino desde el origen a la salida
        path = []
        while current:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path[1]  # Devolver el siguiente paso en el camino

    def is_valid_move(self, x, y):
        # Verificar si la celda a la que se desea mover es válida (dentro del laberinto y no hay paredes)
        if 0 <= x < len(self.maze[0]) and 0 <= y < len(self.maze):
            # Verificar si hay una pared en la dirección deseada
            if not self.maze[y][x].blocked:
                return True
        return False

    def record_visit(self):
        current_cell = (self.x, self.y)
        # Registrar la visita a la nueva celda
        if current_cell not in self.visited_cells:
            self.cell_visits += 1
            self.visited_cells.add(current_cell)

    def draw(self, screen, pixel_size):
        # Dibujar el ratón en rojo
        pygame.draw.ellipse(screen, (255, 0, 0),
                            (self.x * pixel_size + pixel_size // 4,
                             self.y * pixel_size + pixel_size // 4,
                             pixel_size // 2, pixel_size // 2))
import pygame
import heapq

class MinimumSpanningTreesMouse:
    def __init__(self, maze, start_x, start_y, exit_x, exit_y):
        self.name = 'Mouse MinimumSpanningTrees'
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.exit_x = exit_x  # Coordenada de salida
        self.exit_y = exit_y  # Coordenada de salida
        self.movements = 0  # Contador de movimientos
        self.cell_visits = 0  # Contador de visitas a celdas
        self.visited_cells = set()  # Para asegurar que las visitas no se dupliquen
        self.path = []  # Almacena el camino encontrado por Minimum Spanning Trees
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
            print(f"Moviendo a la celda {next_cell}")
            self.movements += 1
            self.record_visit()
        else:
            self.find_path()  # Busca un nuevo camino si no hay

    def find_path(self):
        # Implementación del algoritmo de árboles de expansión mínima (Prim's algorithm)
        start = (self.x, self.y)
        goal = (self.exit_x, self.exit_y)

        # Verificar que las coordenadas de salida no sean None
        if self.exit_x is None or self.exit_y is None:
            print("Error: Las coordenadas de salida no están definidas.")
            return

        # Aquí se busca el árbol de expansión mínima usando Prim
        print(f"Buscando camino desde {start} hasta {goal}")
        self.path = self.prim(start, goal)

    def prim(self, start, goal):
        # Implementación simplificada del algoritmo de Prim para árboles de expansión mínima
        visited = set()
        edges = []
        paths = {start: [start]}

        # Usamos una cola de prioridad para elegir el borde con el menor peso
        heapq.heappush(edges, (0, start, start))  # (peso, celda origen, celda destino)
        visited.add(start)

        while edges:
            # Seleccionar el borde con el menor peso (aunque todos tienen el mismo peso en este caso)
            _, current, new_cell = heapq.heappop(edges)

            if new_cell not in visited:
                visited.add(new_cell)
                self.calculation_count += 1  # Contar la celda procesada
                print(f"Visitando nueva celda: {new_cell}, desde: {current}")

                # Actualizar el camino
                paths[new_cell] = paths[current] + [new_cell]

                # Revisar si se ha llegado al objetivo
                if new_cell == goal:
                    print(f"Camino encontrado: {paths[new_cell]}")
                    return paths[new_cell][1:]  # Excluir la celda de inicio

                # Agregar los vecinos del nuevo nodo a la cola de prioridad
                for neighbor in self.get_neighbors(new_cell):
                    if neighbor not in visited:
                        heapq.heappush(edges, (1, new_cell, neighbor))
                        print(f"Añadiendo vecino a la cola: {neighbor}")

        print("No se encontró camino.")
        return []  # Retorna vacío si no hay un camino

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell

        # Verifica las celdas adyacentes y si no hay paredes en esa dirección
        if x + 1 < len(self.maze[0]) and self.maze[y][x].is_open('E'):  # Este
            neighbors.append((x + 1, y))
        if x - 1 >= 0 and self.maze[y][x].is_open('W'):  # Oeste
            neighbors.append((x - 1, y))
        if y - 1 >= 0 and self.maze[y][x].is_open('N'):  # Norte
            neighbors.append((x, y - 1))
        if y + 1 < len(self.maze) and self.maze[y][x].is_open('S'):  # Sur
            neighbors.append((x, y + 1))

        # Debug: Mostrar vecinos
        print(f"Vecinos válidos de {cell}: {neighbors}")
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

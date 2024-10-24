import heapq
import basemouse

class MouseIA:
    def __init__(self, maze, start_x, start_y, exit_x, exit_y):
        super().__init__(maze, start_x, start_y)
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.path = []  # La lista que almacenará el camino resultante de A*

    def move(self):
        # Si ya se ha calculado el camino, sigue los pasos
        if self.path:
            next_x, next_y = self.path.pop(0)  # Obtener el siguiente paso del camino
            self.x, self.y = next_x, next_y
        else:
            # Calcular la ruta usando A*
            self.path = self.find_shortest_path()

        self.movements += 1
        self.record_visit()

    def find_shortest_path(self):
        start = (self.x, self.y)
        goal = (self.exit_x, self.exit_y)

        # A* requiere una cola de prioridad
        open_list = []
        heapq.heappush(open_list, (0, start))  # (costo estimado, nodo)

        # Diccionarios para almacenar el costo real y el predecesor de cada nodo
        g_cost = {start: 0}  # Costo desde el inicio hasta el nodo
        came_from = {start: None}  # Nodo desde el que llegamos al nodo actual

        while open_list:
            _, current = heapq.heappop(open_list)

            # Si alcanzamos el objetivo, reconstruimos el camino
            if current == goal:
                return self.reconstruct_path(came_from, current)

            # Expandir los vecinos
            for neighbor in self.get_neighbors(current):
                tentative_g_cost = g_cost[current] + 1  # Asumimos un costo de 1 por cada movimiento

                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))
                    came_from[neighbor] = current

        # Si no se encuentra un camino, se retorna una lista vacía
        return []

    def reconstruct_path(self, came_from, current):
        # Reconstruimos el camino desde el objetivo hacia el inicio
        path = []
        while current:
            path.append(current)
            current = came_from[current]
        path.reverse()  # Revertimos la lista para que vaya del inicio al objetivo
        return path

    def heuristic(self, node, goal):
        # Usamos la distancia Manhattan como heurística (distancia en grilla)
        x1, y1 = node
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbors(self, node):
        x, y = node
        neighbors = []

        # Chequear todas las direcciones posibles y si no hay paredes
        if y > 0 and not self.maze[y][x].north:  # Arriba
            neighbors.append((x, y - 1))
        if y < len(self.maze) - 1 and not self.maze[y][x].south:  # Abajo
            neighbors.append((x, y + 1))
        if x > 0 and not self.maze[y][x].west:  # Izquierda
            neighbors.append((x - 1, y))
        if x < len(self.maze[0]) - 1 and not self.maze[y][x].east:  # Derecha
            neighbors.append((x + 1, y))

        return neighbors
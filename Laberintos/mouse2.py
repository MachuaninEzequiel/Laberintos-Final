import pygame
import heapq
from config import DIFFICULTIES

class Mouse:
    def __init__(self, maze, start_x, start_y, difficulty):
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.direction = 'E'  # El ratón empieza dirigiéndose al Este (derecha)
        self.directions = ['E', 'S', 'W', 'N']  # Dirección en el sentido de las agujas del reloj
        self.speed = DIFFICULTIES[difficulty]['speed']

    def move(self):
        # Seguir la pared a la derecha
        if self.can_move_right():
            self.turn_right()
            self.move_forward()
        elif self.can_move_forward():
            self.move_forward()
        else:
            self.turn_left()

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

    def draw(self, screen, pixel_size):
        # Dibujar el ratón en rojo
        pygame.draw.ellipse(screen, (255, 0, 0),
                            (self.x * pixel_size + pixel_size // 4,
                             self.y * pixel_size + pixel_size // 4,
                             pixel_size // 2, pixel_size // 2))
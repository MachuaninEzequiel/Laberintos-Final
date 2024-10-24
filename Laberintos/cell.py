import pygame

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.west = True
        self.north = True
        self.east = True
        self.south = True

    def draw(self, screen, pixelSize):
        i = self.x * pixelSize
        j = self.y * pixelSize

        if self.visited:
            color = (61, 165, 217)
        else:
            color = (35, 100, 170)
        pygame.draw.rect(screen, color, (i, j, pixelSize, pixelSize))

        if self.west:
            pygame.draw.line(screen, (0, 0, 0), (i, j), (i, j + pixelSize), 2)
        if self.north:
            pygame.draw.line(screen, (0, 0, 0), (i, j), (i + pixelSize, j), 2)
        if self.east:
            pygame.draw.line(screen, (0, 0, 0), (i + pixelSize, j), (i + pixelSize, j + pixelSize), 2)
        if self.south:
            pygame.draw.line(screen, (0, 0, 0), (i, j + pixelSize), (i + pixelSize, j + pixelSize), 2)

    def is_open(self, direction):
        if direction == 'E':
            return not self.east
        elif direction == 'W':
            return not self.west
        elif direction == 'N':
            return not self.north
        elif direction == 'S':
            return not self.south
        return False        
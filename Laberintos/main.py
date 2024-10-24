import pygame
import random
import time
from cell import Cell
from mouse import Mouse

# Constantes
W, H = 700, 700
mazeW, mazeH = 32, 32
pixelSize = 22

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

cells = []
stack = []
maze_generated = False
mouse = None
exit_x = None
exit_y = None
mouse_path = []  # Lista para guardar el camino del ratón
start_time = None
end_time = None
timer_running = False
game_over = False  # Variable para determinar si el juego terminó

# Setup inicial
def setup():
    global cells, stack, maze_generated, mouse, exit_x, exit_y, mouse_path, start_time, end_time, timer_running, game_over
    for y in range(mazeH):
        row = []
        for x in range(mazeW):
            row.append(Cell(x, y))
        cells.append(row)

    rx = random.randint(0, mazeW - 1)
    ry = random.randint(0, mazeH - 1)
    
    first = cells[ry][rx]
    first.visited = True
    stack.append(first)

    maze_generated = False
    mouse = None
    mouse_path = []  # Reiniciar la lista del camino del ratón
    start_time = None
    end_time = None
    timer_running = False
    game_over = False  # Reiniciar el estado del juego

def generate_step():
    global maze_generated, mouse, exit_x, exit_y
    if stack:
        current = stack[-1]
        valid = False
        checks = 0

        while not valid and checks < 10:
            checks += 1
            direction = random.randint(0, 3)

            if direction == 0 and current.x > 0:  # WEST
                next_cell = cells[current.y][current.x - 1]
                if not next_cell.visited:
                    current.west = False
                    next_cell.east = False
                    next_cell.visited = True
                    stack.append(next_cell)
                    valid = True

            elif direction == 1 and current.y > 0:  # NORTH
                next_cell = cells[current.y - 1][current.x]
                if not next_cell.visited:
                    current.north = False
                    next_cell.south = False
                    next_cell.visited = True
                    stack.append(next_cell)
                    valid = True

            elif direction == 2 and current.x < mazeW - 1:  # EAST
                next_cell = cells[current.y][current.x + 1]
                if not next_cell.visited:
                    current.east = False
                    next_cell.west = False
                    next_cell.visited = True
                    stack.append(next_cell)
                    valid = True

            elif direction == 3 and current.y < mazeH - 1:  # SOUTH
                next_cell = cells[current.y + 1][current.x]
                if not next_cell.visited:
                    current.south = False
                    next_cell.north = False
                    next_cell.visited = True
                    stack.append(next_cell)
                    valid = True

        if not valid:
            stack.pop()

    if not stack and not maze_generated:
        # El laberinto se ha generado
        maze_generated = True
        
        # Crear el ratón en la esquina inferior izquierda
        mouse = Mouse(cells, 0, mazeH - 1)

        # Generar una salida en una posición aleatoria
        exit_x = random.randint(0, mazeW - 1)
        exit_y = random.randint(0, mazeH - 1)

def draw_mouse_path():
    # Dibujar una línea punteada para representar el camino recorrido
    if len(mouse_path) > 1:
        for i in range(1, len(mouse_path)):
            x1, y1 = mouse_path[i - 1]
            x2, y2 = mouse_path[i]
            if i % 2 == 0:  # Crear una línea punteada
                pygame.draw.line(screen, (255, 255, 255), 
                                 (x1 * pixelSize + pixelSize // 2, y1 * pixelSize + pixelSize // 2),
                                 (x2 * pixelSize + pixelSize // 2, y2 * pixelSize + pixelSize // 2), 2)

def draw():
    screen.fill((0, 0, 0))

    # Dibujar las celdas
    for row in cells:
        for cell in row:
            cell.draw(screen, pixelSize)

    # Dibujar la salida en verde
    if maze_generated:
        pygame.draw.ellipse(screen, (0, 255, 0),
                            (exit_x * pixelSize + pixelSize // 4,
                             exit_y * pixelSize + pixelSize // 4,
                             pixelSize // 2, pixelSize // 2))

    # Dibujar el camino recorrido por el ratón
    draw_mouse_path()

    # Dibujar el ratón si el laberinto está generado y el juego no ha terminado
    if mouse and not game_over:
        mouse.draw(screen, pixelSize)

    # Mostrar el tiempo transcurrido
    if timer_running:
        current_time = time.time() - start_time
        text = font.render(f"Tiempo: {current_time:.2f}s", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    elif end_time:
        final_time = end_time - start_time
        text = font.render(f"Tiempo Final: {final_time:.2f}s", True, (255, 255, 255))
        screen.blit(text, (10, 10))

# Bucle principal
setup()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generar un paso del laberinto por fotograma si el juego no ha terminado
    if not game_over:
        generate_step()

        # Mover el ratón una vez que el laberinto esté generado
        if maze_generated and mouse:
            if not timer_running:
                start_time = time.time()  # Iniciar el cronómetro
                timer_running = True

            mouse.move()
            mouse_path.append((mouse.x, mouse.y))  # Guardar la posición del ratón

            if mouse.check_exit(exit_x, exit_y):
                end_time = time.time()  # Detener el cronómetro
                timer_running = False
                game_over = True  # Detener el juego
                print(f"¡El ratón ha encontrado la salida en {end_time - start_time:.2f} segundos!")

    # Dibujar en pantalla
    draw()
    pygame.display.flip()
    clock.tick(120)  # Controlar la velocidad de generación y movimiento

pygame.quit()
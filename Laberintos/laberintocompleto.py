import pygame
import pygame_gui
import random
import time
import pandas as pd
from cell import Cell
from mouse import Mouse
from mouse1 import Mouse1
from mouseAstar import AStarMouse

# Constantes
W, H = 800, 800
mazeW, mazeH = 32, 32
pixelSize = 25

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

manager = pygame_gui.UIManager((W, H))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

cells = []
stack = []
maze_generated = False
mouse = None
exit_x = None
exit_y = None
boost_positions = []  # Lista para almacenar las posiciones de los boost
mouse_path = []  # Lista para guardar el camino del ratón
start_time = None
end_time = None
timer_running = False
game_over = False

def select_mouse_model():
    screen.fill(BLACK)

    # Creación de botones UI con pygame_gui
    mouse1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((W // 2 - 100, H // 2 - 100), (200, 50)),
                                                text='Mouse',
                                                manager=manager)
    mouse2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((W // 2 - 100, H // 2), (200, 50)),
                                                text='Mouse1',
                                                manager=manager)
    mouse3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((W // 2 - 100, H // 2 + 100), (200, 50)),
                                                text='MouseA*',
                                                manager=manager)

    # Animaciones de texto
    header_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((W // 2 - 200, H // 2 - 200), (400, 50)),
                                            text="Seleccione un modelo de ratón",
                                            manager=manager,
                                            object_id="#header_label")

    selected_mouse = None
    while True:
        time_delta = clock.tick(60) / 1000.0  # Control de tiempo para la animación
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Manejo de eventos de pygame_gui
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == mouse1_button:
                        selected_mouse = Mouse
                    elif event.ui_element == mouse2_button:
                        selected_mouse = Mouse1
                    elif event.ui_element == mouse3_button:
                        selected_mouse = AStarMouse

            # Si se selecciona un ratón, retornarlo y salir del bucle
            if selected_mouse:
                return selected_mouse

        # Actualizar el manager y el renderizado en pantalla
        manager.update(time_delta)
        screen.fill(BLACK)
        manager.draw_ui(screen)

        pygame.display.update()

# Setup inicial
def setup(mouse_class):
    global cells, stack, maze_generated, mouse, exit_x, exit_y, boost_positions, mouse_path, start_time, end_time, timer_running, game_over
    cells.clear()  # Limpiar el laberinto anterior
    for y in range(mazeH):
        row = []
        for x in range(mazeW):
            row.append(Cell(x, y))
        cells.append(row)

    # Establecer la salida en el centro del laberinto
    exit_x = mazeW // 2
    exit_y = mazeH // 2

    first = cells[0][0]  # Empezar desde la esquina superior izquierda
    first.visited = True
    stack.append(first)

    maze_generated = False
    mouse = None
    boost_positions = []  # Reiniciar las posiciones de los boost
    mouse_path = []  # Reiniciar la lista del camino del ratón
    start_time = None
    end_time = None
    timer_running = False
    game_over = False

    if mouse_class == Mouse or mouse_class == Mouse1:
        mouse = mouse_class(cells, 0, mazeH - 1)  # Crear ratón del tipo seleccionado
    else:
        mouse = mouse_class(cells, 0, mazeH - 1, exit_x, exit_y)  # Le estoy pasando las salidas

def generate_step():
    global maze_generated, mouse, exit_x, exit_y, boost_positions
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

        # Generar tres posiciones de boost en el laberinto
        for _ in range(3):
            boost_x = random.randint(0, mazeW - 1)
            boost_y = random.randint(0, mazeH - 1)
            boost_positions.append((boost_x, boost_y))

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

    # Dibujar los boost en naranja
    for (bx, by) in boost_positions:
        pygame.draw.ellipse(screen, (255, 165, 0),
                            (bx * pixelSize + pixelSize // 4,
                             by * pixelSize + pixelSize // 4,
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

# Función para guardar estadísticas
def save_statistics(time_taken, movements, cell_visits):
    data = {
        'modelo': mouse.name, 
        'time': time_taken, 
        'movements': movements, 
        'cell_visits': cell_visits, 
        'boost_count': mouse.boost_count, 
        'Ispeed': mouse.original_speed, 
        'Fspeed': mouse.speed
    }
    df = pd.DataFrame([data])
    df.to_csv('Mouse_Maze_Statistics.csv', mode='a', header=not pd.io.common.file_exists('Mouse_Maze_Statistics.csv'), index=False)

# Bucle principal
mouse_class = select_mouse_model()  # Seleccionar el modelo de ratón
setup(mouse_class)  # Usar el modelo seleccionado

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

            if (mouse.x, mouse.y) in boost_positions:
                mouse.speed_boost()  # Aplicar el boost de velocidad

            if mouse_class == Mouse or mouse_class == Mouse1:
                if mouse.check_exit(exit_x, exit_y):
                    end_time = time.time()  # Detener el cronómetro
                    timer_running = False
                    game_over = True  # Detener el juego

                    # Guardar estadísticas
                    final_time = end_time - start_time
                    save_statistics(final_time, mouse.movements, mouse.cell_visits)

                    print(f"¡El ratón ha encontrado la salida en {final_time:.2f} segundos!")
            else:
                if mouse.check_exit():
                    end_time = time.time()  # Detener el cronómetro
                    timer_running = False
                    game_over = True  # Detener el juego

                    # Guardar estadísticas
                    final_time = end_time - start_time
                    save_statistics(final_time, mouse.movements, mouse.cell_visits)

                    print(f"¡El ratón ha encontrado la salida en {final_time:.2f} segundos!")

    # Dibujar en pantalla
    draw()
    pygame.display.flip()
    clock.tick(120)  # Controlar la velocidad de generación y movimiento del ratón

pygame.quit()

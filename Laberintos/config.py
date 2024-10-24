DIFFICULTIES = {
    'easy': {'speed': 60, 'complexity': 0.2},
    'medium': {'speed': 120, 'complexity': 0.5},
    'hard': {'speed': 180, 'complexity': 0.8}
}

def select_difficulty():
    print("Seleccione un nivel de dificultad:")
    for i, level in enumerate(DIFFICULTIES.keys(), 1):
        print(f"{i}. {level.capitalize()}")
    choice = input("Ingrese el número de la dificultad deseada: ")
    return list(DIFFICULTIES.keys())[int(choice) - 1]  # Retorna la clave de la dificultad elegida

WALL_COLOR = (0, 0, 0)  # Color de las paredes
VISITED_COLOR = (61, 165, 217)  # Color de las celdas visitadas
UNVISITED_COLOR = (35, 100, 170)  # Color de las celdas no visitadas
MOUSE_COLOR = (255, 0, 0)  # Color del ratón
EXIT_COLOR = (0, 255, 0)  # Color de la salida
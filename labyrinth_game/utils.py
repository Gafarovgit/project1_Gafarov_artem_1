"""
Вспомогательные функции игры Лабиринт сокровищ.
"""

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """
    Выводит описание текущей комнаты игрока.
    
    Args:
        game_state (dict): Текущее состояние игры
    """
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    print(f"\n== {current_room_name.upper()} ==")
    print(room['description'])
    
    # Показываем предметы в комнате
    if room['items']:
        print("\nЗаметные предметы:", ", ".join(room['items']))
    else:
        print("\nЗаметные предметы: нет")
    
    # Показываем выходы
    if room['exits']:
        exits_str = ", ".join(room['exits'].keys())
        print(f"Выходы: {exits_str}")
    else:
        print("Выходы: нет")
    
    # Показываем наличие загадки
    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")
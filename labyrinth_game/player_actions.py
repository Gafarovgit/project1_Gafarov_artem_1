"""
Функции для действий игрока.
"""

from labyrinth_game.constants import ROOMS


def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении.
    
    Args:
        game_state (dict): Текущее состояние игры
        direction (str): Направление движения (north, south, east, west)
    
    Returns:
        bool: True если перемещение успешно, False если нет
    """
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем есть ли выход в этом направлении
    if direction in current_room['exits']:
        # Обновляем текущую комнату
        game_state['current_room'] = current_room['exits'][direction]
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        
        print(f"Вы переместились {direction}.")
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """
    Поднимает предмет из текущей комнаты.
    
    Args:
        game_state (dict): Текущее состояние игры
        item_name (str): Название предмета для подбора
    
    Returns:
        bool: True если предмет подобран, False если нет
    """
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем есть ли предмет в комнате
    if item_name in current_room['items']:
        # Добавляем предмет в инвентарь
        game_state['player_inventory'].append(item_name)
        # Удаляем предмет из комнаты
        current_room['items'].remove(item_name)
        
        print(f"Вы подняли: {item_name}")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False
    
def use_item(game_state, item_name):
    """
    Использует предмет из инвентаря.
    
    Args:
        game_state (dict): Текущее состояние игры
        item_name (str): Название предмета для использования
    
    Returns:
        bool: True если предмет использован, False если нет
    """
    # Проверяем есть ли предмет в инвентаре
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return False
    
    # Логика использования для разных предметов
    if item_name == 'torch':
        print("Вы зажигаете факел. Стало светлее!")
        return True
    elif item_name == 'sword':
        print("Вы размахиваете мечом. Чувствуете себя увереннее!")
        return True
    elif item_name == 'rusty_key':
        print("Вы осматриваете ржавый ключ. Он выглядит древним.")
        return True
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
        return False    
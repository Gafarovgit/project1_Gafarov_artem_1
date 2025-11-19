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
        next_room_name = current_room['exits'][direction]
        
        # Проверка доступа в treasure_room
        if next_room_name == 'treasure_room':
            if 'rusty_key' not in game_state['player_inventory']:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False
            else:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        
        # Обновляем текущую комнату
        game_state['current_room'] = next_room_name
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        
        print(f"Вы переместились {direction}.")
        
        # Случайное событие после перемещения
        from labyrinth_game.utils import random_event
        random_event(game_state)
        
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
        # Особый случай - нельзя поднять сундук
        if item_name in ['treasure_chest', 'bank_treasure_chest']:
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return False
            
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
    elif item_name == 'golden_key':
        print("Золотой ключ блестит в свете. Он выглядит очень ценным.")
        return True
    elif item_name == 'coin':
        print("Вы подбрасываете монетку. Она блестит на свету.")
        return True
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
        return False
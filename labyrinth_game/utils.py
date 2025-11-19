"""
Вспомогательные функции игры Лабиринт сокровищ.
"""

import math

from labyrinth_game.constants import COMMANDS, ROOMS


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


def pseudo_random(seed, modulo):
    """
    Псевдослучайный генератор на основе синуса.
    
    Args:
        seed (int): Начальное значение (например, количество шагов)
        modulo (int): Модуль для определения диапазона [0, modulo)
    
    Returns:
        int: Случайное число в диапазоне [0, modulo)
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    """
    Активирует ловушку - игрок теряет случайный предмет или получает урон.
    
    Args:
        game_state (dict): Текущее состояние игры
    """
    print("Ловушка активирована! Пол стал дрожать...")
    
    # Проверяем есть ли предметы в инвентаре
    if game_state['player_inventory']:
        # Выбираем случайный предмет для потери
        inventory_len = len(game_state['player_inventory'])
        item_index = pseudo_random(game_state['steps_taken'], inventory_len)
        lost_item = game_state['player_inventory'].pop(item_index)
        print(f"Вы потеряли: {lost_item}!")
    else:
        # Если инвентарь пуст - игрок получает урон
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < 3:  # 30% шанс поражения
            print("Ловушка нанесла смертельный урон! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам повезло - вы уцелели, но это было близко!")


def random_event(game_state):
    """
    Случайное событие при перемещения между комнатами.
    
    Args:
        game_state (dict): Текущее состояние игры
    """
    # 10% шанс события
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
        
        if event_type == 0:
            # Находка - монетка
            current_room = ROOMS[game_state['current_room']]
            if 'coin' not in current_room['items']:
                current_room['items'].append('coin')
                print("Вы нашли на полу блестящую монетку!")
        
        elif event_type == 1:
            # Испуг - шорох
            print("Вы слышите подозрительный шорох из темноты...")
            if 'sword' in game_state['player_inventory']:
                print("Но ваш меч отпугивает существо.")
        
        elif event_type == 2:
            # Ловушка (только в trap_room без факела)
            if (game_state['current_room'] == 'trap_room' and
                    'torch' not in game_state['player_inventory']):
                print("Вы не заметили ловушку в темноте!")
                trigger_trap(game_state)


def solve_puzzle(game_state):
    """
    Решает загадку в текущей комнате.
    
    Args:
        game_state (dict): Текущее состояние игры
    """
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем есть ли загадка в комнате
    if current_room['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    
    question, correct_answer = current_room['puzzle']
    
    # Выводим вопрос
    print(question)
    
    # Получаем ответ от пользователя
    user_answer = input("Ваш ответ: ").strip().lower()
    
    # Альтернативные варианты ответов
    alternative_answers = {
        '10': ['десять', '10'],
        '862': ['восемьсот шестьдесят два', '862'],
        '15': ['пятнадцать', '15'],
        'тридцать': ['30', 'тридцать'],
        'лук': ['лук'],
        'резонанс': ['резонанс'],
        'обед': ['обед'],
        'киев': ['киев'],
        'шаг шаг шаг': ['шаг шаг шаг']
    }
    
    # Проверяем ответ
    correct_answers = alternative_answers.get(
        correct_answer,
        [correct_answer.lower()]
    )
    
    if user_answer in correct_answers:
        print("Верно! Загадка решена!")
        # Убираем загадку из комнаты
        current_room['puzzle'] = None
        
        # Награда за решение загадки в зависимости от комнаты
        if current_room_name == 'hall':
            print("Пьедестал опускается, открывая проход на север.")
        elif current_room_name == 'trap_room':
            print("Плиты перестали дрожать. Теперь здесь безопасно.")
        
    else:
        print("Неверно. Попробуйте снова.")
        # Особый случай - ловушка в trap_room при неверном ответе
        if current_room_name == 'trap_room':
            print("Плиты содрогаются!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """
    Пытается открыть сундук с сокровищами.
    
    Args:
        game_state (dict): Текущее состояние игры
    """
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем что игрок в комнате с сокровищами и есть сундук
    if (current_room_name != 'treasure_room' and
            current_room_name != 'bank_treasure_room'):
        print("Здесь нет сундука с сокровищами.")
        return
    
    has_treasure = 'treasure_chest' in current_room['items']
    has_bank_treasure = 'bank_treasure_chest' in current_room['items']
    
    if not has_treasure and not has_bank_treasure:
        print("Сундук с сокровищами уже открыт!")
        return
    
    # Проверяем есть ли ключ у игрока
    has_rusty_key = 'rusty_key' in game_state['player_inventory']
    has_golden_key = 'golden_key' in game_state['player_inventory']
    
    if has_rusty_key or has_golden_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из комнаты
        if 'treasure_chest' in current_room['items']:
            current_room['items'].remove('treasure_chest')
        if 'bank_treasure_chest' in current_room['items']:
            current_room['items'].remove('bank_treasure_chest')
        
        print("🎉 В сундуке сокровище! Вы победили! 🎉")
        game_state['game_over'] = True
        return
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. У вас нет ключа.")
    if current_room['puzzle'] is not None:
        use_code = input("Попробовать ввести код? (да/нет): ").strip().lower()
        if use_code == 'да':
            question, correct_answer = current_room['puzzle']
            print(f"\n{question}")
            user_code = input("Введите код: ").strip()
            
            if user_code == correct_answer:
                print("🎉 Код верный! Сундук открыт! Вы победили! 🎉")
                # Удаляем сундук из комнаты
                if 'treasure_chest' in current_room['items']:
                    current_room['items'].remove('treasure_chest')
                if 'bank_treasure_chest' in current_room['items']:
                    current_room['items'].remove('bank_treasure_chest')
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остается запертым.")
        else:
            print("Вы отступаете от сундука.")
    else:
        print("Нет возможности открыть сундук без ключа.")


def show_help():
    """
    Показывает список доступных команд.
    """
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")
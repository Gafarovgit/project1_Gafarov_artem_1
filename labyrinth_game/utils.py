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
    
    # Проверяем ответ
    if user_answer == correct_answer.lower():
        print("Верно! Загадка решена!")
        # Убираем загадку из комнаты
        current_room['puzzle'] = None
        # Можно добавить награду здесь
    else:
        print("Неверно. Попробуйте снова.")

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
    
    if 'treasure_chest' not in current_room['items'] and 'bank_treasure_chest' not in current_room['items']:
        print("Сундук с сокровищами уже открыт!")
        return
    
    # Проверяем есть ли ключ у игрока
    if 'rusty_key' in game_state['player_inventory'] or 'golden_key' in game_state['player_inventory']:
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
        use_code = input("Ввести код? (да/нет): ").strip().lower()
        if use_code == 'да':
            question, correct_answer = current_room['puzzle']
            print(question)
            user_code = input("Код: ").strip()
            
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
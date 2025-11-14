#!/usr/bin/env python3
"""
Главный модуль игры Лабиринт сокровищ.
Точка входа в приложение.
"""

# Импортируем созданные модули и данные
from labyrinth_game.constants import ROOMS
from labyrinth_game import player_actions
from labyrinth_game import utils


def create_initial_game_state():
    """
    Создает начальное состояние игры.
    
    Returns:
        dict: Начальное состояние игры
    """
    return {
        'player_inventory': [],      # Инвентарь игрока
        'current_room': 'entrance',  # Стартовая комната
        'game_over': False,          # Флаг окончания игры
        'steps_taken': 0             # Счетчик шагов
    }


def main():
    """Основная функция игры."""
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    # cоздаем начальное состояние игры
    game_state = create_initial_game_state()
    
    # Показываем стартовую комнату
    utils.describe_current_room(game_state)
    
    print("\nИгра началась! Введите 'help' для списка команд.")
    
    # Основной игровой цикл
    while not game_state['game_over']:
        try:
            # Получаем команду от пользователя
            command = input("\n> ").strip().lower()
            
            # Обрабатываем базовые команды
            if command in ['quit', 'exit', 'q']:
                print("Спасибо за игру! До свидания!")
                game_state['game_over'] = True
            elif command == 'help':
                print("\nДоступные команды:")
                print("  go <direction> - перейти в направлении (north/south/east/west)")
                print("  take <item> - поднять предмет")
                print("  use <item> - использовать предмет из инвентаря")
                print("  look - осмотреть текущую комнату")
                print("  inventory - показать инвентарь")
                print("  solve - попытаться решить загадку или открыть сундук")
                print("  help - показать это сообщение")
                print("  quit - выйти из игры")
            elif command == 'look':
                utils.describe_current_room(game_state)
            elif command == 'inventory':
                if game_state['player_inventory']:
                    print("Ваш инвентарь:", ", ".join(game_state['player_inventory']))
                else:
                    print("Ваш инвентарь пуст.")
            elif command.startswith('go '):
                # звлекаем направление из команды
                direction = command[3:].strip()  # Убираем 'go '
                player_actions.move_player(game_state, direction)
                # После перемещения показываем новую комнату
                utils.describe_current_room(game_state)
            elif command.startswith('take '):
                # Извлекаем название предмета
                item_name = command[5:].strip()  # Убираем 'take '
                player_actions.take_item(game_state, item_name)
            elif command.startswith('use '):
                # Извлекаем название предмета
                item_name = command[4:].strip()  # Убираем 'use '
                player_actions.use_item(game_state, item_name)
            elif command == 'solve':
                # Если игрок в комнате с скровищами, пытаемся открыть сундук
                if (game_state['current_room'] == 'treasure_room' or 
                    game_state['current_room'] == 'bank_treasure_room'):
                    utils.attempt_open_treasure(game_state)
                else:
                    utils.solve_puzzle(game_state)
            else:
                print(f"Неизвестная команда: '{command}'. Введите 'help' для списка команд.")
                
        except (KeyboardInterrupt, EOFError):
            print("\n\nВыход из игры. До свидания!")
            game_state['game_over'] = True
    
    print("Игра завершена.")


if __name__ == "__main__":
    # Код выплняется только при прямом запуске модуля
    main()
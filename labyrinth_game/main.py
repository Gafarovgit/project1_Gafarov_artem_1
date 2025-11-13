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
    
    # Создаем начальное состояние игры
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
                print("  look - осмотреть текущую комнату")
                print("  inventory - показать инвентарь") 
                print("  help - показать это сообщение")
                print("  quit - выйти из игры")
            elif command == 'look':
                utils.describe_current_room(game_state)
            elif command == 'inventory':
                if game_state['player_inventory']:
                    print("Ваш инвентарь:", ", ".join(game_state['player_inventory']))
                else:
                    print("Ваш инвентарь пуст.")
            else:
                print(f"Неизвестная команда: '{command}'. Введите 'help' для списка команд.")
                
        except (KeyboardInterrupt, EOFError):
            print("\n\nВыход из игры. До свидания!")
            game_state['game_over'] = True
    
    print("Игра завершена.")


if __name__ == "__main__":
    # Код выполняется только при прямом запуске модуля
    main()
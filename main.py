"""
Главный модуль программы "Обработка точек" с улучшенной обработкой исключений.
Все в одном файле для простоты.
"""

import logging
import math
import random
import sys


# ========== КАСТОМНЫЕ ИСКЛЮЧЕНИЯ ==========
class PointsException(Exception):
    """Базовое исключение для всех ошибок."""
    pass


class InputError(PointsException):
    """Ошибки ввода."""
    pass


class ProcessingError(PointsException):
    """Ошибки обработки."""
    pass


# ========== ТЕКСТОВЫЕ СООБЩЕНИЯ (для локализации) ==========
TEXTS = {
    # Меню
    "menu_title": "ГЛАВНОЕ МЕНЮ",
    "menu_options": [
        "Тест всех функций",
        "Обработать точки (ручной ввод)",
        "Обработать точки (случайные)",
        "Сравнить все методы",
        "Управление логированием",
        "Выход"
    ],
    
    # Методы
    "method_title": "Выберите метод обработки:",
    "methods": [
        "Оригинальный (ближайшая по расстоянию)",
        "Последовательный (следующая точка)",
        "Минимальная сумма координат",
        "Минимальная координата X"
    ],
    
    # Ввод
    "input_title": "Ручной ввод",
    "input_format": "Формат: x,y (например: 3,4)",
    "input_exit": "Для выхода введите 'стоп'",
    "input_prompt": "Точка {count}: ",
    
    # Ошибки
    "errors": {
        "invalid_format": "Некорректный формат: '{input}'. Нужно: x,y",
        "invalid_number": "Не число: '{value}'",
        "empty_list": "Нет точек для обработки",
        "invalid_choice": "Некорректный выбор: '{choice}'",
        "invalid_method": "Неизвестный метод: '{method}'"
    },
    
    # Логирование
    "logging_menu": [
        "INFO - все действия",
        "WARNING - только предупреждения",
        "ERROR - только ошибки",
        "CRITICAL - почти ничего",
        "Показать текущий уровень"
    ]
}


# ========== ОСНОВНЫЕ ФУНКЦИИ ==========
def calc_dist(p1, p2):
    """Вычисляет расстояние между точками."""
    try:
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    except (TypeError, ValueError) as e:
        raise ProcessingError(f"Ошибка расстояния: {p1} - {p2}") from e


def find_closest(target, points):
    """Находит ближайшую точку."""
    if len(points) <= 1:
        return None
    
    try:
        other_points = [p for p in points if p != target]
        if not other_points:
            return None
        return min(other_points, key=lambda p: calc_dist(target, p))
    except Exception as e:
        raise ProcessingError(f"Ошибка поиска ближайшей") from e


def add_points(p1, p2):
    """Складывает две точки."""
    try:
        return (p1[0] + p2[0], p1[1] + p2[1])
    except (TypeError, IndexError) as e:
        raise ProcessingError(f"Ошибка сложения: {p1} + {p2}") from e


def process_points(points, method):
    """Обрабатывает точки выбранным методом."""
    if not points:
        raise ProcessingError(TEXTS["errors"]["empty_list"])
    
    if method == "original":
        # Ближайшая по расстоянию
        result = []
        for p in points:
            closest = find_closest(p, points)
            result.append(add_points(p, closest) if closest else p)
        return result
    
    elif method == "sequential":
        # Следующая точка
        result = []
        n = len(points)
        for i in range(n):
            next_point = points[(i + 1) % n]
            result.append(add_points(points[i], next_point))
        return result
    
    elif method == "min_sum":
        # Минимальная сумма координат
        special = min(points, key=lambda p: p[0] + p[1])
        return [add_points(p, special) for p in points]
    
    elif method == "min_x":
        # Минимальная координата X
        special = min(points, key=lambda p: p[0])
        return [add_points(p, special) for p in points]
    
    else:
        raise ProcessingError(TEXTS["errors"]["invalid_method"].format(method=method))


# ========== ВВОД ДАННЫХ ==========
def input_points_manual():
    """Ручной ввод точек."""
    points = []
    print(f"\n=== {TEXTS['input_title']} ===")
    print(TEXTS["input_format"])
    print(TEXTS["input_exit"])
    
    count = 1
    while True:
        try:
            user = input(TEXTS["input_prompt"].format(count=count)).strip()
            
            if user.lower() in ['стоп', 'stop', '']:
                break
            
            # Простая валидация
            if ',' not in user:
                raise InputError(TEXTS["errors"]["invalid_format"].format(input=user))
            
            x_str, y_str = user.split(',', 1)
            
            try:
                x = float(x_str.strip())
            except ValueError:
                raise InputError(TEXTS["errors"]["invalid_number"].format(value=x_str))
            
            try:
                y = float(y_str.strip())
            except ValueError:
                raise InputError(TEXTS["errors"]["invalid_number"].format(value=y_str))
            
            points.append((x, y))
            count += 1
            
        except InputError as e:
            print(f"Ошибка: {e}")
            continue
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            continue
    
    print(f"Введено точек: {len(points)}")
    return points


def make_random_points(n=5):
    """Создает случайные точки."""
    points = []
    for _ in range(n):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        points.append((x, y))
    
    print(f"Создано {n} случайных точек")
    return points


# ========== ЛОГИРОВАНИЕ ==========
def setup_logging(level=logging.INFO):
    """Настраивает логирование."""
    logger = logging.getLogger('points_app')
    logger.setLevel(level)
    
    # Очистка старых обработчиков
    if logger.handlers:
        logger.handlers.clear()
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Файл
    file_handler = logging.FileHandler('app.log', encoding='utf-8', mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    # Консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Логирование запущено (уровень: {logging.getLevelName(level)})")
    return logger


# ========== ОСНОВНОЙ КОД ==========
def show_menu():
    """Показывает главное меню."""
    print("\n" + "="*50)
    print(TEXTS["menu_title"])
    print("="*50)
    
    for i, option in enumerate(TEXTS["menu_options"], 1):
        print(f"{i}. {option}")


def choose_method():
    """Выбор метода обработки."""
    print(f"\n{TEXTS['method_title']}")
    for i, method in enumerate(TEXTS["methods"], 1):
        print(f"{i}. {method}")
    
    choice = input("Ваш выбор (1-4): ").strip()
    
    methods_map = {
        "1": "original",
        "2": "sequential",
        "3": "min_sum",
        "4": "min_x"
    }
    
    if choice not in methods_map:
        raise InputError(TEXTS["errors"]["invalid_choice"].format(choice=choice))
    
    return methods_map[choice]


def test_all(logger):
    """Тестирует все функции."""
    logger.info("Запуск тестов")
    
    print("\n=== Тест функций ===")
    
    # Тест расстояния
    dist = calc_dist((0, 0), (3, 4))
    print(f"1. Расстояние: {dist:.1f} (должно быть 5.0)")
    
    # Тест ближайшей
    points = [(0, 0), (2, 0), (5, 5)]
    closest = find_closest((0, 0), points)
    print(f"2. Ближайшая: {closest} (должно быть (2,0))")
    
    # Тест сложения
    sum_pts = add_points((1, 2), (3, 4))
    print(f"3. Сложение: {sum_pts} (должно быть (4,6))")
    
    # Тест методов
    test_pts = [(1, 1), (4, 5), (2, 3)]
    print(f"\nТестовые точки: {test_pts}")
    
    for method_name in ["original", "sequential", "min_sum", "min_x"]:
        result = process_points(test_pts, method_name)
        print(f"4. Метод '{method_name}': {result}")


def compare_methods(logger):
    """Сравнивает все методы."""
    logger.info("Сравнение методов")
    
    print("\n=== Сравнение методов ===")
    points = [(0, 0), (3, 0), (1, 2), (4, 1)]
    print(f"Точки: {points}")
    
    print("\nРезультаты:")
    print("-" * 40)
    
    for method_name in ["original", "sequential", "min_sum", "min_x"]:
        print(f"\nМетод: {method_name}")
        result = process_points(points, method_name)
        
        if method_name == "original":
            for i, p in enumerate(points):
                closest = find_closest(p, points)
                if closest:
                    print(f"  {p} + {closest} = {result[i]}")
        elif method_name == "sequential":
            for i in range(len(points)):
                next_idx = (i + 1) % len(points)
                print(f"  {points[i]} + {points[next_idx]} = {result[i]}")
        else:
            special = min(points, key=lambda p: p[0] + p[1]) if method_name == "min_sum" else min(points, key=lambda p: p[0])
            for i, p in enumerate(points):
                print(f"  {p} + {special} = {result[i]}")


def manage_logging(logger):
    """Управление логированием."""
    print("\n=== Управление логированием ===")
    for i, option in enumerate(TEXTS["logging_menu"], 1):
        print(f"{i}. {option}")
    
    choice = input("Выберите: ").strip()
    
    levels = {
        "1": logging.INFO,
        "2": logging.WARNING,
        "3": logging.ERROR,
        "4": logging.CRITICAL
    }
    
    if choice == "5":
        current = logging.getLevelName(logger.getEffectiveLevel())
        print(f"Текущий уровень: {current}")
        return
    
    if choice in levels:
        level = levels[choice]
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
        
        logger.info(f"Уровень изменен на {logging.getLevelName(level)}")
        print(f"Установлен уровень: {logging.getLevelName(level)}")
    else:
        print("Неверный выбор")


def main():
    """Главная функция."""
    # Настройка логирования
    logger = setup_logging(logging.INFO)
    
    print("ПРОГРАММА: Обработка точек")
    print("К каждой точке прибавить ближайшую (разные методы)")
    print("Логи записываются в app.log")
    
    try:
        while True:
            show_menu()
            choice = input("\nВыберите: ").strip()
            
            logger.info(f"Пользователь выбрал: {choice}")
            
            try:
                if choice == "1":
                    test_all(logger)
                
                elif choice == "2":
                    points = input_points_manual()
                    if points:
                        method = choose_method()
                        result = process_points(points, method)
                        
                        print("\nРезультат:")
                        for i in range(len(points)):
                            print(f"  {points[i]} -> {result[i]}")
                        logger.info(f"Обработано {len(points)} точек")
                
                elif choice == "3":
                    try:
                        n = int(input("Сколько точек? ") or "5")
                        points = make_random_points(n)
                        method = choose_method()
                        result = process_points(points, method)
                        
                        print("\nРезультат:")
                        for i in range(len(points)):
                            print(f"  {points[i]} -> {result[i]}")
                        logger.info(f"Обработано {n} случайных точек")
                    except ValueError:
                        print("Ошибка! Нужно число.")
                        logger.error("Неверный ввод количества точек")
                
                elif choice == "4":
                    compare_methods(logger)
                
                elif choice == "5":
                    manage_logging(logger)
                
                elif choice == "6":
                    print("\nВыход из программы. Пока!")
                    logger.info("Программа завершена")
                    break
                
                else:
                    print("Неверный выбор. Попробуйте снова.")
                    logger.warning(f"Неверный выбор: {choice}")
            
            except (InputError, ProcessingError) as e:
                print(f"Ошибка: {e}")
                logger.error(f"Ошибка: {e}")
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                logger.exception(f"Неожиданная ошибка: {e}")
    
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана")
        logger.info("Программа прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        logger.exception(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
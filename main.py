"""
Главный модуль программы "Обработка точек" с логированием.

Предоставляет интерактивный интерфейс для работы с различными
алгоритмами обработки точек. Включает меню, тестирование функций
и сравнение методов.

Usage:
    python main.py
"""

import logging
from distance import calc_dist, find_closest
from points import add_two_points, process_points, process_sequential, process_with_min_point
from input_data import input_by_hand, make_random_points


# ========== КОНФИГУРАЦИЯ ЛОГИРОВАНИЯ ==========

def setup_logging(level=logging.INFO):
    """
    Настраивает систему логирования для проекта.
    
    Parameters
    ----------
    level : int, optional
        Уровень логирования (по умолчанию INFO)
    
    Returns
    -------
    logging.Logger
        Сконфигурированный логгер
    """
    logger = logging.getLogger('points_processor')
    logger.setLevel(level)
    
    # Очищаем предыдущие обработчики
    if logger.handlers:
        logger.handlers.clear()
    
    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для файла
    file_handler = logging.FileHandler('app.log', encoding='utf-8', mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Логирование настроено с уровнем {logging.getLevelName(level)}")
    
    return logger

def log_user_action(action):
    """
    Логирует действие пользователя.
    
    Parameters
    ----------
    action : str
        Описание действия пользователя
    """
    logger = logging.getLogger('points_processor')
    logger.info(f"ПОЛЬЗОВАТЕЛЬ: {action}")

def log_function_call(func_name, **kwargs):
    """
    Логирует вызов функции.
    
    Parameters
    ----------
    func_name : str
        Имя функции
    **kwargs : dict
        Аргументы функции
    """
    logger = logging.getLogger('points_processor')
    
    # Формируем строку с аргументами
    args_str = ''
    if kwargs:
        args_list = []
        for k, v in kwargs.items():
            if isinstance(v, list) and len(v) > 3:
                args_list.append(f"{k}=[...]({len(v)} точек)")
            else:
                args_list.append(f"{k}={v}")
        args_str = ', '.join(args_list)
    
    logger.info(f"ФУНКЦИЯ: {func_name}({args_str})")


# Инициализация логгера
logger = setup_logging(logging.INFO)


# ========== ОСНОВНЫЕ ФУНКЦИИ ==========

def show_menu():
    """
    Отображает главное меню программы.
    
    Returns
    -------
    None
        Функция только выводит информацию на экран
    
    Notes
    -----
    Меню использует форматирование для лучшей читаемости.
    Все опции пронумерованы для удобства выбора.
    """
    log_user_action("Показано главное меню")
    print("\n" + "="*50)
    print("ГЛАВНОЕ МЕНЮ")
    print("="*50)
    print("1. Тест всех функций (все методы)")
    print("2. Обработать точки (ручной ввод)")
    print("3. Обработать точки (случайные)")
    print("4. Сравнить все методы на примере")
    print("5. Управление логированием")
    print("6. Выход")


def choose_method():
    """
    Отображает меню выбора метода обработки.
    
    Returns
    -------
    str
        Выбор пользователя (от "1" до "4")
    
    Note
    ----
    Функция не проверяет корректность ввода - это делает method_name()
    """
    log_user_action("Показано меню выбора метода")
    print("\nВыберите метод обработки:")
    print("1. Оригинальный (ближайшая по расстоянию)")
    print("2. Последовательный (следующая точка в массиве)")
    print("3. Минимальная сумма координат (x+y)")
    print("4. Минимальная координата X")
    return input("Ваш выбор (1-4): ").strip()


def method_name(choice):
    """
    Преобразует выбор пользователя в имя метода.
    
    Parameters
    ----------
    choice : str
        Выбор пользователя из меню choose_method()
    
    Returns
    -------
    str
        Имя метода для передачи в process_points()
    
    Examples
    --------
    >>> method_name("1")
    'original'
    >>> method_name("3")
    'min_sum'
    
    Note
    ----
    Если передан неизвестный выбор, возвращается "original"
    """
    methods = {
        "1": "original",
        "2": "sequential",
        "3": "min_sum",
        "4": "min_x"
    }
    return methods.get(choice, "original")


def test_all():
    """
    Выполняет комплексное тестирование всех функций проекта.
    
    Returns
    -------
    None
        Результаты тестов выводятся на экран
    
    Notes
    -----
    Функция проверяет:
    1. Корректность вычисления расстояний
    2. Работу поиска ближайшей точки
    3. Корректность сложения точек
    4. Работу всех четырех алгоритмов обработки
    """
    log_user_action("Запущено тестирование всех функций")
    log_function_call("test_all")
    
    print("\n=== Тест всех функций ===")
    
    # Тест расстояния
    d = calc_dist((0,0), (3,4))
    print(f"1. calc_dist: {d:.1f} (должно быть 5.0)")
    logger.debug(f"Тест calc_dist: результат={d}")
    
    # Тест ближайшей точки
    pts = [(0,0), (2,0), (5,5)]
    c = find_closest((0,0), pts)
    print(f"2. find_closest: {c} (должно быть (2,0))")
    logger.debug(f"Тест find_closest: результат={c}")
    
    # Тест сложения
    s = add_two_points((1,2), (3,4))
    print(f"3. add_two_points: {s} (должно быть (4,6))")
    logger.debug(f"Тест add_two_points: результат={s}")
    
    # Тест всех методов обработки
    test_points = [(1, 1), (4, 5), (2, 3)]
    print(f"\nТестовые точки: {test_points}")
    logger.debug(f"Тестовые точки: {test_points}")
    
    methods = [
        ("Оригинальный", "original"),
        ("Последовательный", "sequential"),
        ("Минимальная сумма", "min_sum"),
        ("Минимальный X", "min_x")
    ]
    
    for name, method in methods:
        result = process_points(test_points, method)
        print(f"4. {name}: {result}")
        logger.debug(f"Тест метода {name}: результат={result}")


def process_with_method(points, method_choice=None):
    """
    Обрабатывает точки выбранным методом с дополнительной информацией.
    
    Parameters
    ----------
    points : list
        Список точек для обработки
    method_choice : str, optional
        Предварительный выбор метода, если None - запрашивается у пользователя
    
    Returns
    -------
    list
        Результат обработки точек
    
    Note
    ----
    Для методов min_sum и min_x дополнительно выводится информация
    о выбранной "особой" точке.
    """
    if method_choice is None:
        method_choice = choose_method()
    
    method = method_name(method_choice)
    
    log_function_call("process_with_method", 
                     points_count=len(points),
                     method=method)
    
    # Специальная информация для некоторых методов
    if method == "min_sum":
        min_point = min(points, key=lambda p: p[0] + p[1])
        print(f"Минимальная сумма координат у точки: {min_point} (сумма={min_point[0]+min_point[1]})")
        logger.debug(f"Точка с минимальной суммой: {min_point}")
    elif method == "min_x":
        min_point = min(points, key=lambda p: p[0])
        print(f"Минимальная координата X у точки: {min_point}")
        logger.debug(f"Точка с минимальным X: {min_point}")
    
    result = process_points(points, method)
    logger.debug(f"Результат обработки: {result}")
    
    return result


def compare_methods():
    """
    Сравнивает все методы обработки на фиксированном наборе точек.
    
    Returns
    -------
    None
        Результаты сравнения выводятся на экран
    
    Notes
    -----
    Используется фиксированный набор точек для наглядности сравнения.
    Для каждого метода показывается:
    1. Название метода
    2. Логика работы
    3. Промежуточные вычисления
    4. Итоговый результат
    """
    log_user_action("Запущено сравнение методов")
    log_function_call("compare_methods")
    
    print("\n=== Сравнение всех методов ===")
    
    # Используем фиксированный набор для наглядности
    points = [(0, 0), (3, 0), (1, 2), (4, 1)]
    print(f"Точки для сравнения: {points}")
    logger.debug(f"Точки для сравнения: {points}")
    
    print("\nРезультаты:")
    print("-" * 60)
    
    # Оригинальный метод
    result = process_points(points, "original")
    print("1. Оригинальный (ближайшая по расстоянию):")
    for i, p in enumerate(points):
        closest = find_closest(p, points)
        if closest:
            print(f"   {p} + {closest} = {result[i]}")
            logger.debug(f"Оригинальный: {p} + {closest} = {result[i]}")
    
    # Последовательный метод
    result = process_points(points, "sequential")
    print("\n2. Последовательный (следующая точка):")
    for i in range(len(points)):
        next_idx = (i + 1) % len(points)
        print(f"   {points[i]} + {points[next_idx]} = {result[i]}")
        logger.debug(f"Последовательный: {points[i]} + {points[next_idx]} = {result[i]}")
    
    # Минимальная сумма
    result = process_points(points, "min_sum")
    min_sum_point = min(points, key=lambda p: p[0] + p[1])
    print(f"\n3. Минимальная сумма координат (x+y):")
    print(f"   Базовая точка: {min_sum_point}")
    logger.debug(f"Минимальная сумма: базовая точка {min_sum_point}")
    for i, p in enumerate(points):
        print(f"   {p} + {min_sum_point} = {result[i]}")
        logger.debug(f"Минимальная сумма: {p} + {min_sum_point} = {result[i]}")
    
    # Минимальный X
    result = process_points(points, "min_x")
    min_x_point = min(points, key=lambda p: p[0])
    print(f"\n4. Минимальная координата X:")
    print(f"   Базовая точка: {min_x_point}")
    logger.debug(f"Минимальный X: базовая точка {min_x_point}")
    for i, p in enumerate(points):
        print(f"   {p} + {min_x_point} = {result[i]}")
        logger.debug(f"Минимальный X: {p} + {min_x_point} = {result[i]}")


def manage_logging():
    """
    Управление уровнем логирования программы.
    
    Returns
    -------
    None
        Изменяет уровень логирования во время выполнения
    """
    log_user_action("Открыто управление логированием")
    
    print("\n=== Управление логированием ===")
    print("1. INFO - логировать все действия")
    print("2. WARNING - только предупреждения и ошибки")
    print("3. ERROR - только ошибки")
    print("4. CRITICAL - только критические ошибки")
    print("5. Показать текущий уровень")
    
    choice = input("Ваш выбор (1-5): ").strip()
    log_user_action(f"Выбор уровня логирования: {choice}")
    
    current_level = logging.getLevelName(logger.getEffectiveLevel())
    
    if choice == "1":
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            handler.setLevel(logging.INFO)
        print("Установлен уровень INFO - логирование всех действий")
        logger.info("Уровень логирования изменен на INFO")
    elif choice == "2":
        logger.setLevel(logging.WARNING)
        for handler in logger.handlers:
            handler.setLevel(logging.WARNING)
        print("Установлен уровень WARNING - только предупреждения и ошибки")
        logger.warning("Уровень логирования изменен на WARNING")
    elif choice == "3":
        logger.setLevel(logging.ERROR)
        for handler in logger.handlers:
            handler.setLevel(logging.ERROR)
        print("Установлен уровень ERROR - только ошибки")
        logger.error("Уровень логирования изменен на ERROR")
    elif choice == "4":
        logger.setLevel(logging.CRITICAL)
        for handler in logger.handlers:
            handler.setLevel(logging.CRITICAL)
        print("Установлен уровень CRITICAL - только критические ошибки")
        logger.critical("Уровень логирования изменен на CRITICAL. Логирование практически отключено.")
    elif choice == "5":
        print(f"Текущий уровень логирования: {current_level}")
    else:
        print("Неверный выбор. Текущий уровень не изменен.")


def main():
    """
    Основная функция программы - точка входа.
    
    Returns
    -------
    None
    
    Notes
    -----
    Функция реализует бесконечный цикл меню до выбора опции "Выход".
    Обрабатывает все возможные варианты ввода пользователя.
    """
    log_function_call("main")
    
    print("ПРОЕКТ: Обработка точек")
    print("Задание: К каждой точке прибавить ближайшую (разные методы)")
    print("Логирование включено. Логи сохраняются в файл app.log")
    
    while True:
        show_menu()
        choice = input("\nВыберите: ").strip()
        
        log_user_action(f"Выбор в главном меню: {choice}")
        
        if choice == "1":
            test_all()
        
        elif choice == "2":
            log_function_call("input_by_hand")
            points = input_by_hand()
            if len(points) > 0:
                result = process_with_method(points)
                print("\nРезультат:")
                for i in range(len(points)):
                    print(f"  {points[i]} -> {result[i]}")
                logger.info(f"Обработано {len(points)} точек")
        
        elif choice == "3":
            try:
                n = int(input("Сколько точек? ") or "5")
                log_user_action(f"Создание {n} случайных точек")
                log_function_call("make_random_points", n=n)
                points = make_random_points(n)
                result = process_with_method(points)
                print("\nРезультат:")
                for i in range(len(points)):
                    print(f"  {points[i]} -> {result[i]}")
                logger.info(f"Обработано {n} случайных точек")
            except ValueError:
                print("Ошибка! Используйте целое число.")
                logger.error("Ошибка при вводе количества точек")
        
        elif choice == "4":
            compare_methods()
        
        elif choice == "5":
            manage_logging()
        
        elif choice == "6":
            log_user_action("Выход из программы")
            print("\nВыход из программы. До свидания!")
            logger.info("Программа завершена")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")
            logger.warning(f"Неверный выбор в меню: {choice}")


if __name__ == "__main__":
    main()
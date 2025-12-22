"""
Главный модуль программы "Обработка точек".

Предоставляет интерактивный интерфейс для работы с различными
алгоритмами обработки точек. Включает меню, тестирование функций
и сравнение методов.

Usage:
    python main.py
"""

from distance import calc_dist, find_closest
from points import add_two_points, process_points, process_sequential, process_with_min_point
from input_data import input_by_hand, make_random_points

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
    print("\n" + "="*50)
    print("ГЛАВНОЕ МЕНЮ")
    print("="*50)
    print("1. Тест всех функций (все методы)")
    print("2. Обработать точки (ручной ввод)")
    print("3. Обработать точки (случайные)")
    print("4. Сравнить все методы на примере")
    print("5. Выход")


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
    print("\n=== Тест всех функций ===")
    
    # Тест расстояния
    d = calc_dist((0,0), (3,4))
    print(f"1. calc_dist: {d:.1f} (должно быть 5.0)")
    
    # Тест ближайшей точки
    pts = [(0,0), (2,0), (5,5)]
    c = find_closest((0,0), pts)
    print(f"2. find_closest: {c} (должно быть (2,0))")
    
    # Тест сложения
    s = add_two_points((1,2), (3,4))
    print(f"3. add_two_points: {s} (должно быть (4,6))")
    
    # Тест всех методов обработки
    test_points = [(1, 1), (4, 5), (2, 3)]
    print(f"\nТестовые точки: {test_points}")
    
    methods = [
        ("Оригинальный", "original"),
        ("Последовательный", "sequential"),
        ("Минимальная сумма", "min_sum"),
        ("Минимальный X", "min_x")
    ]
    
    for name, method in methods:
        result = process_points(test_points, method)
        print(f"4. {name}: {result}")


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
    
    # Специальная информация для некоторых методов
    if method == "min_sum":
        min_point = min(points, key=lambda p: p[0] + p[1])
        print(f"Минимальная сумма координат у точки: {min_point} (сумма={min_point[0]+min_point[1]})")
    elif method == "min_x":
        min_point = min(points, key=lambda p: p[0])
        print(f"Минимальная координата X у точки: {min_point}")
    
    result = process_points(points, method)
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
    print("\n=== Сравнение всех методов ===")
    
    # Используем фиксированный набор для наглядности
    points = [(0, 0), (3, 0), (1, 2), (4, 1)]
    print(f"Точки для сравнения: {points}")
    
    print("\nРезультаты:")
    print("-" * 60)
    
    # Оригинальный метод
    result = process_points(points, "original")
    print("1. Оригинальный (ближайшая по расстоянию):")
    for i, p in enumerate(points):
        closest = find_closest(p, points)
        if closest:
            print(f"   {p} + {closest} = {result[i]}")
    
    # Последовательный метод
    result = process_points(points, "sequential")
    print("\n2. Последовательный (следующая точка):")
    for i in range(len(points)):
        next_idx = (i + 1) % len(points)
        print(f"   {points[i]} + {points[next_idx]} = {result[i]}")
    
    # Минимальная сумма
    result = process_points(points, "min_sum")
    min_sum_point = min(points, key=lambda p: p[0] + p[1])
    print(f"\n3. Минимальная сумма координат (x+y):")
    print(f"   Базовая точка: {min_sum_point}")
    for i, p in enumerate(points):
        print(f"   {p} + {min_sum_point} = {result[i]}")
    
    # Минимальный X
    result = process_points(points, "min_x")
    min_x_point = min(points, key=lambda p: p[0])
    print(f"\n4. Минимальная координата X:")
    print(f"   Базовая точка: {min_x_point}")
    for i, p in enumerate(points):
        print(f"   {p} + {min_x_point} = {result[i]}")


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
    print("ПРОЕКТ: Обработка точек")
    print("Задание: К каждой точке прибавить ближайшую (разные методы)")
    
    while True:
        show_menu()
        choice = input("\nВыберите: ").strip()
        
        if choice == "1":
            test_all()
        
        elif choice == "2":
            points = input_by_hand()
            if len(points) > 0:
                result = process_with_method(points)
                print("\nРезультат:")
                for i in range(len(points)):
                    print(f"  {points[i]} -> {result[i]}")
        
        elif choice == "3":
            try:
                n = int(input("Сколько точек? ") or "5")
                points = make_random_points(n)
                result = process_with_method(points)
                print("\nРезультат:")
                for i in range(len(points)):
                    print(f"  {points[i]} -> {result[i]}")
            except ValueError:
                print("Ошибка! Используйте целое число.")
        
        elif choice == "4":
            compare_methods()
        
        elif choice == "5":
            print("\nВыход из программы. До свидания!")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
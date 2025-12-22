from distance import find_closest
import math

"""
МОДУЛЬ ОБРАБОТКИ ТОЧЕК
Содержит 4 алгоритма определения "ближайшей" точки

Доступные методы:
1. "original" - ближайшая по расстоянию (O(n²))
2. "sequential" - следующая точка в массиве (O(n))
3. "min_sum" - точка с минимальной суммой координат (O(n))
4. "min_x" - точка с минимальной координатой X (O(n))

Основные функции:
- process_points(points, method="original") - универсальная функция
- add_two_points(p1, p2) - сложение двух точек
"""

def add_two_points(p1, p2):
    """Складывает две точки"""
    return (p1[0] + p2[0], p1[1] + p2[1])

# Оригинальная функция
def process_all_points(points):
    """К каждой точке прибавляет ближайшую (по расстоянию)"""
    result = []
    
    for p in points:
        closest = find_closest(p, points)
        
        if closest:
            new_point = add_two_points(p, closest)
        else:
            new_point = p  # Если точка одна
        
        result.append(new_point)
    
    return result

# Вариант 1: Последовательный сосед
def process_sequential(points):
    """К каждой точке прибавляет следующую в массиве"""
    if not points:
        return []
    
    result = []
    n = len(points)
    
    for i in range(n):
        # Берем следующую точку (для последней - первую)
        next_point = points[(i + 1) % n]
        result.append(add_two_points(points[i], next_point))
    
    return result

# Вариант 2: Сумма с минимальной по координатам
def process_with_min_point(points, use_sum=True):
    """
    К каждой точке прибавляет точку с минимальными координатами
    use_sum=True: минимальная сумма координат (x+y)
    use_sum=False: минимальная координата x
    """
    if not points:
        return []
    
    # Выбираем критерий для нахождения "особой" точки
    if use_sum:
        # Минимальная сумма координат
        special_point = min(points, key=lambda p: p[0] + p[1])
    else:
        # Минимальная координата x (при равных x - минимальная y)
        special_point = min(points, key=lambda p: (p[0], p[1]))
    
    # Ко всем прибавляем эту одну точку
    return [add_two_points(p, special_point) for p in points]

# Новая функция для выбора метода обработки
def process_points(points, method="original"):
    """Обрабатывает точки указанным методом"""
    if method == "original":
        return process_all_points(points)
    elif method == "sequential":
        return process_sequential(points)
    elif method == "min_sum":
        return process_with_min_point(points, use_sum=True)
    elif method == "min_x":
        return process_with_min_point(points, use_sum=False)
    else:
        raise ValueError(f"Неизвестный метод: {method}")
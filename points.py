"""
Модуль алгоритмов обработки точек.

Предоставляет 4 различных алгоритма для определения "ближайшей" точки
и выполнения операции сложения точек.

Доступные методы:
1. original - ближайшая по евклидову расстоянию (O(n²))
2. sequential - следующая точка в массиве (O(n))
3. min_sum - точка с минимальной суммой координат (O(n))
4. min_x - точка с минимальной координатой X (O(n))
"""

from distance import find_closest


def add_two_points(p1, p2):
    """
    Складывает координаты двух точек.
    
    Выполняет поэлементное сложение координат:
    result = (p1.x + p2.x, p1.y + p2.y)
    
    Parameters
    ----------
    p1 : tuple
        Первая точка (x1, y1)
    p2 : tuple
        Вторая точка (x2, y2)
    
    Returns
    -------
    tuple
        Результирующая точка
    
    Examples
    --------
    >>> add_two_points((1, 2), (3, 4))
    (4, 6)
    >>> add_two_points((-1, 5), (2, -3))
    (1, 2)
    """
    return (p1[0] + p2[0], p1[1] + p2[1])


def process_all_points(points):
    """
    Оригинальный алгоритм: к каждой точке прибавляет ближайшую по расстоянию.
    
    Для каждой точки в массиве находит ближайшую (по евклидову расстоянию)
    среди остальных точек и выполняет сложение.
    
    Parameters
    ----------
    points : list
        Список точек для обработки
    
    Returns
    -------
    list
        Список результирующих точек
    
    Note
    ----
    Временная сложность: O(n²) из-за попарного сравнения всех точек.
    Не рекомендуется для массивов с более чем 1000 точек.
    """
    result = []
    
    for p in points:
        closest = find_closest(p, points)
        
        if closest:
            new_point = add_two_points(p, closest)
        else:
            new_point = p  # Если точка одна
        
        result.append(new_point)
    
    return result


def process_sequential(points):
    """
    Последовательный алгоритм: каждая точка складывается со следующей.
    
    Точки обрабатываются в порядке их следования в массиве.
    Последняя точка складывается с первой (кольцевая обработка).
    
    Parameters
    ----------
    points : list
        Список точек для обработки
    
    Returns
    -------
    list
        Список результирующих точек
    
    Examples
    --------
    >>> process_sequential([(1, 1), (2, 2), (3, 3)])
    [(3, 3), (5, 5), (4, 4)]
    
    Note
    ----
    Временная сложность: O(n). Самый быстрый алгоритм.
    Подходит для обработки упорядоченных последовательностей.
    """
    if not points:
        return []
    
    result = []
    n = len(points)
    
    for i in range(n):
        # Берем следующую точку (для последней - первую)
        next_point = points[(i + 1) % n]
        result.append(add_two_points(points[i], next_point))
    
    return result


def process_with_min_point(points, use_sum=True):
    """
    Алгоритм с минимальной точкой: все точки складываются с одной "особой" точкой.
    
    Parameters
    ----------
    points : list
        Список точек для обработки
    use_sum : bool, optional
        Если True - используется точка с минимальной суммой координат (x+y)
        Если False - используется точка с минимальной координатой X
        По умолчанию True
    
    Returns
    -------
    list
        Список результирующих точек
    
    Examples
    --------
    >>> points = [(3, 5), (1, 2), (4, 1)]
    >>> process_with_min_point(points, use_sum=True)
    [(4, 7), (2, 4), (5, 3)]  # Минимальная сумма у (1, 2) = 3
    
    >>> process_with_min_point(points, use_sum=False)
    [(4, 7), (2, 4), (5, 3)]  # Минимальный X у (1, 2)
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


def process_points(points, method="original"):
    """
    Универсальная функция для выбора метода обработки точек.
    
    Parameters
    ----------
    points : list
        Список точек для обработки
    method : str, optional
        Метод обработки:
        - "original": ближайшая по расстоянию
        - "sequential": следующая точка в массиве
        - "min_sum": точка с минимальной суммой координат
        - "min_x": точка с минимальной координатой X
        По умолчанию "original"
    
    Returns
    -------
    list
        Список результирующих точек
    
    Raises
    ------
    ValueError
        Если указан неизвестный метод
    
    Examples
    --------
    >>> points = [(1, 1), (4, 5), (2, 3)]
    >>> process_points(points, "original")
    [(2, 3), (7, 7), (4, 5)]
    >>> process_points(points, "sequential")
    [(5, 6), (6, 8), (3, 4)]
    """
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
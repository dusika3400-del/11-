import math

"""
МОДУЛЬ ВЫЧИСЛЕНИЯ РАССТОЯНИЙ
Содержит функции для работы с геометрическими расстояниями

Функции:
- calc_dist(p1, p2) -> float
  Вычисляет евклидово расстояние между двумя точками
  
- find_closest(target, points) -> tuple или None
  Находит ближайшую точку к заданной
  Возвращает None если точек меньше 2
"""

def calc_dist(p1, p2):
    """Вычисляет расстояние между двумя точками"""
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def find_closest(target, points):
    """Находит ближайшую точку к заданной"""
    if len(points) <= 1:
        return None
    
    # Убираем саму точку из списка
    other_points = [p for p in points if p != target]
   
    if not other_points:
        return None
    
    # Ищем точку с минимальным расстоянием
    closest = min(other_points, key=lambda p: calc_dist(target, p))
    return closest
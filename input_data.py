import random

"""
МОДУЛЬ ВВОДА ДАННЫХ
Функции для получения точек

Функции:
- input_by_hand() -> list
  Интерактивный ввод с клавиатуры
  
- make_random_points(n=5) -> list
  Генерация n случайных точек в диапазоне [-10, 10]
"""

def input_by_hand():
    """Ручной ввод точек"""
    points = []
    print("\n=== Ручной ввод ===")
    print("Формат: x,y  (например: 3,4)")
    print("Для выхода введите 'стоп'")
    
    count = 1
    while True:
        user = input(f"Точка {count}: ").strip()
        
        if user.lower() in ['стоп', 'stop', '']:
            break
        
        try:
            parts = user.split(',')
            if len(parts) != 2:
                print("Ошибка: нужны 2 числа через запятую")
                continue
            
            x = float(parts[0])
            y = float(parts[1])
            points.append((x, y))
            count += 1
            
        except:
            print("Ошибка: введите числа!")
    
    print(f"Введено точек: {len(points)}")
    return points

def make_random_points(n=5):
    """Создает случайные точки"""
    points = []
    for i in range(n):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        points.append((x, y))
    
    print(f"Создано {n} случайных точек")
    return points
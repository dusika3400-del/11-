from distance import calc_dist, find_closest

print("=== Тест ветки branch1-distance ===")

# Тест 1: расстояние
p1 = (0, 0)
p2 = (3, 4)
d = calc_dist(p1, p2)
print(f"1. Расстояние ({p1}) -> ({p2}) = {d}")
print(f"   Ожидалось: 5.0, Тест: {'Пройден' if abs(d-5)<0.001 else 'Не пройден'}")

# Тест 2: ближайшая точка
points = [(0,0), (5,0), (2,2), (10,10)]
close = find_closest((0,0), points)
print(f"\n2. Ближайшая к (0,0) в {points}")
print(f"   Результат: {close}")
print(f"   Ожидалось: (2,2), Тест: {'Пройден' if close==(2,2) else 'Не пройден'}")

print("\nТесты завершены!")
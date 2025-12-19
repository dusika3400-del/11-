from points import add_two_points, process_all_points

print("=== Тест ветки branch2-points ===")

# Тест 1: сложение точек
p1 = (1, 2)
p2 = (3, 4)
sum_point = add_two_points(p1, p2)
print(f"1. Сложение: ({p1}) + ({p2}) = {sum_point}")
print(f"   Ожидалось: (4,6), Тест: {'Пройден' if sum_point==(4,6) else 'Не пройден'}")

# Тест 2: обработка массива
test_points = [(0,0), (3,0), (1,1)]
processed = process_all_points(test_points)
print(f"\n2. Обработка массива: {test_points}")
print(f"   Результат: {processed}")

print("\nТесты завершены!")
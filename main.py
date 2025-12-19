from distance import calc_dist, find_closest
from points import add_two_points, process_all_points
from input_data import input_by_hand, make_random_points

def show_menu():
    """Главное меню"""
    print("\n" + "="*40)
    print("ГЛАВНОЕ МЕНЮ")
    print("="*40)
    print("1. Тест всех функций")
    print("2. Обработать точки (ручной ввод)")
    print("3. Обработать точки (случайные)")
    print("4. Выход")

def test_all():
    """Тестирует все функции"""
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
    
    # Тест обработки
    r = process_all_points([(0,0), (2,0), (5,5)])
    print(f"4. process_all_points: {r}")

def main():
    """Основная функция"""
    print("ПРОЕКТ: Обработка точек")
    print("Задание: К каждой точке прибавить ближайшую")
    
    while True:
        show_menu()
        choice = input("Выберите: ")
        
        if choice == "1":
            test_all()
        
        elif choice == "2":
            points = input_by_hand()
            if points:
                result = process_all_points(points)
                print("\nРезультат:")
                for i in range(len(points)):
                    print(f"  {points[i]} -> {result[i]}")
        
        elif choice == "3":
            try:
                n = int(input("Сколько точек? ") or "5")
                points = make_random_points(n)
                result = process_all_points(points)
                print("\nРезультат:")
                for i in range(len(points)):
                    print(f"  {points[i]} -> {result[i]}")
            except:
                print("Ошибка!")
        
        elif choice == "4":
            print("Выход")
            break
        
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()
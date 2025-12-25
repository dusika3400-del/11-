"""
Главный модуль программы "Обработка точек" с автоматным программированием.
Реализация через словарь переходов (jump table).
"""

import logging
import math
import random
import sys
from datetime import datetime
from enum import Enum

# ========== ОПРЕДЕЛЕНИЕ СОСТОЯНИЙ АВТОМАТА ==========
class AppState(Enum):
    """Состояния конечного автомата приложения."""
    INITIAL = "initial"          # Начальное состояние
    MAIN_MENU = "main_menu"      # Главное меню
    TEST_FUNCTIONS = "test_functions"  # Тестирование
    INPUT_METHOD = "input_method"      # Выбор метода ввода
    MANUAL_INPUT = "manual_input"      # Ручной ввод
    RANDOM_INPUT = "random_input"      # Случайные точки
    CHOOSE_METHOD = "choose_method"    # Выбор метода обработки
    PROCESS_POINTS = "process_points"  # Обработка точек
    COMPARE_METHODS = "compare_methods"  # Сравнение методов
    LOGGING_MENU = "logging_menu"      # Меню логирования
    EXIT = "exit"                      # Выход
    ERROR = "error"                    # Ошибка


# ========== ТЕКСТОВЫЕ СООБЩЕНИЯ ==========
TEXTS = {
    "menu_title": "ГЛАВНОЕ МЕНЮ",
    "menu_options": [
        "Тест всех функций",
        "Обработать точки (ручной ввод)",
        "Обработать точки (случайные)",
        "Сравнить все методы",
        "Управление логированием",
        "Выход"
    ],
    
    "method_title": "Выберите метод обработки:",
    "methods": [
        "Оригинальный (ближайшая по расстоянию)",
        "Последовательный (следующая точка)",
        "Минимальная сумма координат",
        "Минимальная координата X"
    ],
    
    "logging_menu": [
        "INFO - все действия",
        "WARNING - только предупреждения",
        "ERROR - только ошибки",
        "CRITICAL - почти ничего",
        "Показать текущий уровень"
    ]
}


# ========== ОСНОВНЫЕ ФУНКЦИИ ОБРАБОТКИ ТОЧЕК ==========
def calc_dist(p1, p2):
    """Вычисляет расстояние между точками."""
    try:
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    except (TypeError, ValueError) as e:
        raise Exception(f"Ошибка расстояния: {p1} - {p2}") from e


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
        raise Exception(f"Ошибка поиска ближайшей") from e


def add_points(p1, p2):
    """Складывает две точки."""
    try:
        return (p1[0] + p2[0], p1[1] + p2[1])
    except (TypeError, IndexError) as e:
        raise Exception(f"Ошибка сложения: {p1} + {p2}") from e


def process_points(points, method):
    """Обрабатывает точки выбранным методом."""
    if not points:
        raise Exception("Нет точек для обработки")
    
    method_handlers = {
        "original": lambda: [add_points(p, find_closest(p, points) or p) for p in points],
        "sequential": lambda: [add_points(points[i], points[(i + 1) % len(points)]) for i in range(len(points))],
        "min_sum": lambda: [add_points(p, min(points, key=lambda x: x[0] + x[1])) for p in points],
        "min_x": lambda: [add_points(p, min(points, key=lambda x: x[0])) for p in points]
    }
    
    if method not in method_handlers:
        raise Exception(f"Неизвестный метод: {method}")
    
    return method_handlers[method]()


# ========== КОНЕЧНЫЙ АВТОМАТ ПРИЛОЖЕНИЯ ==========
class PointsApplicationFSM:
    """
    Конечный автомат для управления приложением обработки точек.
    Реализован через словарь переходов (jump table).
    """
    
    def __init__(self):
        """Инициализация автомата."""
        self.state = AppState.INITIAL
        self.logger = None
        self.context = {
            'points': [],
            'method': None,
            'error': None,
            'choice': None
        }
        
        # Таблица переходов: (текущее_состояние, вход) -> (новое_состояние, обработчик)
        self.transitions = {
            # Инициализация
            (AppState.INITIAL, None): (AppState.MAIN_MENU, self.handle_initial),
            
            # Главное меню
            (AppState.MAIN_MENU, '1'): (AppState.TEST_FUNCTIONS, self.handle_test),
            (AppState.MAIN_MENU, '2'): (AppState.INPUT_METHOD, self.handle_input_method),
            (AppState.MAIN_MENU, '3'): (AppState.RANDOM_INPUT, self.handle_random_input),
            (AppState.MAIN_MENU, '4'): (AppState.COMPARE_METHODS, self.handle_compare),
            (AppState.MAIN_MENU, '5'): (AppState.LOGGING_MENU, self.handle_logging_menu),
            (AppState.MAIN_MENU, '6'): (AppState.EXIT, self.handle_exit),
            
            # Ввод метода
            (AppState.INPUT_METHOD, '1'): (AppState.MANUAL_INPUT, self.handle_manual_input),
            (AppState.INPUT_METHOD, '2'): (AppState.RANDOM_INPUT, self.handle_random_input),
            
            # После ввода точек -> выбор метода обработки
            (AppState.MANUAL_INPUT, 'done'): (AppState.CHOOSE_METHOD, self.handle_choose_method),
            (AppState.RANDOM_INPUT, 'done'): (AppState.CHOOSE_METHOD, self.handle_choose_method),
            
            # После выбора метода -> обработка
            (AppState.CHOOSE_METHOD, '1'): (AppState.PROCESS_POINTS, self.handle_process_points),
            (AppState.CHOOSE_METHOD, '2'): (AppState.PROCESS_POINTS, self.handle_process_points),
            (AppState.CHOOSE_METHOD, '3'): (AppState.PROCESS_POINTS, self.handle_process_points),
            (AppState.CHOOSE_METHOD, '4'): (AppState.PROCESS_POINTS, self.handle_process_points),
            
            # После обработки -> главное меню
            (AppState.PROCESS_POINTS, 'done'): (AppState.MAIN_MENU, self.handle_return_to_menu),
            (AppState.TEST_FUNCTIONS, 'done'): (AppState.MAIN_MENU, self.handle_return_to_menu),
            (AppState.COMPARE_METHODS, 'done'): (AppState.MAIN_MENU, self.handle_return_to_menu),
            (AppState.LOGGING_MENU, 'done'): (AppState.MAIN_MENU, self.handle_return_to_menu),
            
            # Ошибка
            (AppState.ERROR, 'retry'): (AppState.MAIN_MENU, self.handle_error_recovery),
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """Настройка логирования."""
        self.logger = logging.getLogger('points_fsm')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            
            file_handler = logging.FileHandler('fsm_app.log', encoding='utf-8', mode='a')
            file_handler.setFormatter(formatter)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        self.logger.info(f"Автомат запущен. Начальное состояние: {self.state}")
    
    def transition(self, input_symbol):
        """
        Выполняет переход между состояниями.
        
        Args:
            input_symbol: Входной символ (выбор пользователя)
        
        Returns:
            Кортеж (новое_состояние, результат_обработки)
        """
        self.context['choice'] = input_symbol
        
        # Логирование перехода
        self.logger.info(f"Переход: {self.state} + '{input_symbol}'")
        
        # Поиск перехода в таблице
        key = (self.state, input_symbol)
        
        if key in self.transitions:
            new_state, handler = self.transitions[key]
            self.logger.info(f"Найден переход: {self.state} -> {new_state}")
            
            # Выполняем обработчик перехода
            try:
                result = handler()
                self.state = new_state
                self.logger.info(f"Успешный переход в состояние: {self.state}")
                return new_state, result
            except Exception as e:
                self.logger.error(f"Ошибка в обработчике {handler.__name__}: {e}")
                self.state = AppState.ERROR
                self.context['error'] = str(e)
                return AppState.ERROR, f"Ошибка: {e}"
        else:
            # Недопустимый переход
            error_msg = f"Недопустимый переход из {self.state} с входом '{input_symbol}'"
            self.logger.warning(error_msg)
            return self.state, error_msg
    
    # ========== ОБРАБОТЧИКИ ПЕРЕХОДОВ ==========
    
    def handle_initial(self):
        """Обработчик начального состояния."""
        print("=" * 60)
        print("ПРОГРАММА: Обработка точек (автоматная реализация)")
        print("К каждой точке прибавить ближайшую (разные методы)")
        print("=" * 60)
        return "Автомат инициализирован"
    
    def handle_test(self):
        """Тестирование всех функций."""
        self.logger.info("Запуск тестирования функций")
        
        print("\n" + "="*40)
        print("ТЕСТИРОВАНИЕ ВСЕХ ФУНКЦИЙ")
        print("="*40)
        
        # Тест 1: Расстояние
        dist = calc_dist((0, 0), (3, 4))
        print(f"1. Расстояние (0,0)-(3,4): {dist:.1f} (должно быть 5.0)")
        
        # Тест 2: Ближайшая точка
        points = [(0, 0), (2, 0), (5, 5)]
        closest = find_closest((0, 0), points)
        print(f"2. Ближайшая к (0,0): {closest} (должно быть (2,0))")
        
        # Тест 3: Сложение
        sum_pts = add_points((1, 2), (3, 4))
        print(f"3. Сложение (1,2)+(3,4): {sum_pts} (должно быть (4,6))")
        
        # Тест 4: Все методы
        test_pts = [(1, 1), (4, 5), (2, 3)]
        print(f"\nТестовые точки: {test_pts}")
        
        for method_name in ["original", "sequential", "min_sum", "min_x"]:
            result = process_points(test_pts, method_name)
            print(f"4. Метод '{method_name}': {result}")
        
        print("\nНажмите Enter для возврата в меню...")
        input()
        return 'done'
    
    def handle_input_method(self):
        """Выбор метода ввода точек."""
        print("\n=== Выбор метода ввода ===")
        print("1. Ручной ввод")
        print("2. Случайная генерация")
        print("0. Назад")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == '0':
            self.state = AppState.MAIN_MENU
            return "Возврат в меню"
        
        return choice
    
    def handle_manual_input(self):
        """Ручной ввод точек."""
        print("\n=== РУЧНОЙ ВВОД ТОЧЕК ===")
        print("Формат: x,y  (например: 3,4)")
        print("Для завершения введите 'готово'")
        
        points = []
        count = 1
        
        while True:
            try:
                user = input(f"Точка {count}: ").strip()
                
                if user.lower() in ['готово', 'готов', 'done', '']:
                    break
                
                if ',' not in user:
                    print("Ошибка: используйте формат x,y")
                    continue
                
                x_str, y_str = user.split(',', 1)
                x = float(x_str.strip())
                y = float(y_str.strip())
                
                points.append((x, y))
                count += 1
                
            except ValueError:
                print("Ошибка: введите числа")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        self.context['points'] = points
        print(f"Введено {len(points)} точек")
        
        if points:
            return 'done'
        else:
            print("Нет точек для обработки")
            self.state = AppState.MAIN_MENU
            return "Нет точек"
    
    def handle_random_input(self):
        """Генерация случайных точек."""
        print("\n=== ГЕНЕРАЦИЯ СЛУЧАЙНЫХ ТОЧЕК ===")
        
        try:
            n = int(input("Сколько точек создать? (по умолчанию 5): ") or "5")
            points = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(n)]
            
            self.context['points'] = points
            print(f"Создано {n} случайных точек:")
            for i, p in enumerate(points, 1):
                print(f"  {i}. {p}")
            
            return 'done'
        except ValueError:
            print("Ошибка: нужно ввести число")
            self.state = AppState.MAIN_MENU
            return "Ошибка ввода"
    
    def handle_choose_method(self):
        """Выбор метода обработки."""
        if not self.context['points']:
            print("Нет точек для обработки")
            self.state = AppState.MAIN_MENU
            return "Нет точек"
        
        print("\n=== ВЫБОР МЕТОДА ОБРАБОТКИ ===")
        print("1. Оригинальный (ближайшая по расстоянию)")
        print("2. Последовательный (следующая точка)")
        print("3. Минимальная сумма координат")
        print("4. Минимальная координата X")
        print("0. Назад")
        
        choice = input("Ваш выбор (1-4): ").strip()
        
        if choice == '0':
            self.state = AppState.MAIN_MENU
            return "Возврат в меню"
        
        # Сохраняем выбор метода
        methods = {'1': 'original', '2': 'sequential', '3': 'min_sum', '4': 'min_x'}
        if choice in methods:
            self.context['method'] = methods[choice]
            return choice
        else:
            print("Неверный выбор")
            return self.handle_choose_method()
    
    def handle_process_points(self):
        """Обработка точек выбранным методом."""
        points = self.context['points']
        method = self.context['method']
        
        if not points or not method:
            print("Ошибка: нет данных для обработки")
            self.state = AppState.MAIN_MENU
            return "Нет данных"
        
        print(f"\n=== ОБРАБОТКА ТОЧЕК МЕТОДОМ '{method}' ===")
        print(f"Точки: {points}")
        
        try:
            result = process_points(points, method)
            
            print("\nРезультаты:")
            print("-" * 30)
            
            # Вывод в зависимости от метода
            if method == 'original':
                for i, p in enumerate(points):
                    closest = find_closest(p, points)
                    print(f"  {p} + {closest if closest else p} = {result[i]}")
            elif method == 'sequential':
                n = len(points)
                for i in range(n):
                    next_idx = (i + 1) % n
                    print(f"  {points[i]} + {points[next_idx]} = {result[i]}")
            else:
                special = min(points, key=lambda p: p[0] + p[1]) if method == 'min_sum' else min(points, key=lambda p: p[0])
                for i, p in enumerate(points):
                    print(f"  {p} + {special} = {result[i]}")
            
            print("\nИтоговый результат:")
            print(f"  {result}")
            
            self.logger.info(f"Обработано {len(points)} точек методом {method}")
            
            print("\nНажмите Enter для продолжения...")
            input()
            return 'done'
            
        except Exception as e:
            print(f"Ошибка обработки: {e}")
            self.logger.error(f"Ошибка обработки: {e}")
            return 'error'
    
    def handle_compare(self):
        """Сравнение всех методов обработки."""
        print("\n" + "="*40)
        print("СРАВНЕНИЕ ВСЕХ МЕТОДОВ ОБРАБОТКИ")
        print("="*40)
        
        # Используем стандартные точки или вводим
        print("1. Использовать стандартные точки")
        print("2. Ввести свои точки")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == '1':
            points = [(0, 0), (3, 0), (1, 2), (4, 1)]
        elif choice == '2':
            # Простой ввод
            points = []
            print("Введите точки в формате x,y (пустая строка - завершение):")
            while True:
                user = input("Точка: ").strip()
                if not user:
                    break
                if ',' in user:
                    try:
                        x, y = map(float, user.split(','))
                        points.append((x, y))
                    except ValueError:
                        print("Ошибка: введите числа")
        else:
            print("Неверный выбор")
            return 'error'
        
        if not points:
            print("Нет точек для сравнения")
            return 'error'
        
        print(f"\nТочки для сравнения: {points}")
        print("\nРезультаты:")
        print("-" * 50)
        
        methods = ['original', 'sequential', 'min_sum', 'min_x']
        method_names = {
            'original': 'Оригинальный',
            'sequential': 'Последовательный', 
            'min_sum': 'Минимальная сумма',
            'min_x': 'Минимальный X'
        }
        
        for method in methods:
            print(f"\n{method_names[method]}:")
            try:
                result = process_points(points, method)
                print(f"  Результат: {result}")
            except Exception as e:
                print(f"  Ошибка: {e}")
        
        print("\nНажмите Enter для продолжения...")
        input()
        return 'done'
    
    def handle_logging_menu(self):
        """Меню управления логированием."""
        print("\n=== УПРАВЛЕНИЕ ЛОГИРОВАНИЕМ ===")
        print("1. INFO - все действия")
        print("2. WARNING - только предупреждения")
        print("3. ERROR - только ошибки")
        print("4. CRITICAL - почти ничего")
        print("5. Показать текущий уровень")
        print("0. Назад")
        
        choice = input("Выберите: ").strip()
        
        if choice == '0':
            return 'done'
        
        level_map = {
            '1': logging.INFO,
            '2': logging.WARNING,
            '3': logging.ERROR,
            '4': logging.CRITICAL
        }
        
        if choice == '5':
            current = logging.getLevelName(self.logger.getEffectiveLevel())
            print(f"Текущий уровень логирования: {current}")
            return 'continue'
        
        if choice in level_map:
            level = level_map[choice]
            self.logger.setLevel(level)
            for handler in self.logger.handlers:
                handler.setLevel(level)
            
            level_name = logging.getLevelName(level)
            print(f"Установлен уровень логирования: {level_name}")
            self.logger.info(f"Уровень логирования изменен на {level_name}")
            return 'done'
        else:
            print("Неверный выбор")
            return 'continue'
    
    def handle_exit(self):
        """Выход из программы."""
        print("\n" + "="*40)
        print("Выход из программы")
        print("Спасибо за использование!")
        print("="*40)
        self.logger.info("Программа завершена пользователем")
        return 'exit'
    
    def handle_return_to_menu(self):
        """Возврат в главное меню."""
        # Сбрасываем контекст (кроме логгера)
        self.context['points'] = []
        self.context['method'] = None
        self.context['error'] = None
        return 'menu'
    
    def handle_error_recovery(self):
        """Восстановление после ошибки."""
        error = self.context['error']
        print(f"\nПроизошла ошибка: {error}")
        print("Возврат в главное меню...")
        self.context['error'] = None
        return 'recovered'
    
    def show_main_menu(self):
        """Отображение главного меню."""
        print("\n" + "="*50)
        print("ГЛАВНОЕ МЕНЮ (Автоматное программирование)")
        print("="*50)
        
        for i, option in enumerate(TEXTS["menu_options"], 1):
            print(f"{i}. {option}")
        
        print(f"\nТекущее состояние автомата: {self.state.value}")
        print("-" * 50)
    
    def run(self):
        """Основной цикл работы автомата."""
        self.logger.info("Запуск основного цикла автомата")
        
        # Начальный переход
        self.transition(None)
        
        while self.state != AppState.EXIT:
            try:
                if self.state == AppState.MAIN_MENU:
                    self.show_main_menu()
                    choice = input("\nВыберите пункт меню (1-6): ").strip()
                    self.transition(choice)
                
                elif self.state == AppState.ERROR:
                    print(f"\nОШИБКА: {self.context.get('error', 'Неизвестная ошибка')}")
                    choice = input("Введите 'retry' для возврата в меню: ").strip()
                    self.transition(choice)
                
                else:
                    # Для других состояний продолжаем цикл
                    pass
                
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                self.logger.info("Программа прервана по Ctrl+C")
                self.state = AppState.EXIT
                break
            except Exception as e:
                print(f"\nКритическая ошибка: {e}")
                self.logger.exception(f"Критическая ошибка в основном цикле: {e}")
                self.state = AppState.ERROR
                self.context['error'] = str(e)


# ========== ТОЧКА ВХОДА ==========
def main():
    """Главная функция."""
    print("=" * 60)
    print("РЕАЛИЗАЦИЯ АВТОМАТНОГО ПРОГРАММИРОВАНИЯ")
    print("Программа обработки точек через конечный автомат")
    print("=" * 60)
    
    # Создаем и запускаем автомат
    fsm = PointsApplicationFSM()
    fsm.run()


if __name__ == "__main__":
    main()
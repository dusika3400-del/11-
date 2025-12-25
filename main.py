"""
Главный модуль программы "Обработка точек" с автоматным программированием.
Реализация через корутины (coroutines) по принципам из PDF-файла.
"""

import logging
import math
import random
import sys
from exceptions import (
    InvalidInputFormatException, InvalidNumberException,
    EmptyPointsListException, InvalidMethodException,
    InvalidMenuChoiceException
)
from distance import calc_dist, find_closest
from points import add_two_points, process_points
from input_data import input_by_hand, make_random_points


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def prime(coroutine):
    """Декоратор для инициализации корутины."""
    def wrapper(*args, **kwargs):
        cr = coroutine(*args, **kwargs)
        next(cr)  # "Заправка" корутины до первого yield
        return cr
    return wrapper


def setup_logging(level=logging.INFO):
    """Настраивает логирование."""
    logger = logging.getLogger('points_coroutine')
    logger.setLevel(level)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        file_handler = logging.FileHandler('coroutine_app.log', encoding='utf-8', mode='a')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# ========== КОНЕЧНЫЙ АВТОМАТ НА КОРУТИНАХ ==========
class CoroutineFSM:
    """
    Конечный автомат для программы обработки точек.
    Реализован через корутины, как описано в PDF-файле.
    """
    
    def __init__(self):
        self.logger = setup_logging(logging.INFO)
        self.stopped = False
        self.result = None
        
        # Инициализация корутин-состояний
        self.start = self._create_start()
        self.main_menu = self._create_main_menu()
        self.test_functions = self._create_test_functions()
        self.input_method = self._create_input_method()
        self.manual_input = self._create_manual_input()
        self.random_input = self._create_random_input()
        self.choose_method = self._create_choose_method()
        self.process_points_state = self._create_process_points()
        self.compare_methods = self._create_compare_methods()
        self.logging_menu = self._create_logging_menu()
        self.exit_state = self._create_exit()
        self.error_state = self._create_error()
        
        # Текущее состояние
        self.current_state = self.start
        
        # Контекст автомата
        self.context = {
            'points': [],
            'method': None,
            'error': None,
            'choice': None,
            'awaiting_input': False
        }
        
        self.logger.info("Автомат на корутинах инициализирован")
    
    def send(self, char):
        """Отправляет входной символ в текущую корутину-состояние."""
        if self.stopped:
            return
        
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True
            self.logger.warning("Автомат остановлен (StopIteration)")
        except Exception as e:
            self.logger.error(f"Ошибка в корутине: {e}")
            self.current_state = self.error_state
            self.context['error'] = str(e)
    
    def get_user_input(self, prompt="\nВыберите: "):
        """Получает ввод от пользователя с выводом подсказки."""
        return input(prompt).strip()
    
    def run(self):
        """Запускает основной цикл автомата."""
        self.logger.info("Запуск автомата")
        
        # Начальная "заправка" - переход в главное меню
        self.send(None)
        
        try:
            while not self.stopped and self.current_state != self.exit_state:
                # Определяем, в каком состоянии мы находимся
                current_state_name = self._get_state_name(self.current_state)
                
                # Для состояний, которые требуют ввода от пользователя
                if current_state_name in ['main_menu', 'input_method', 'choose_method', 'logging_menu']:
                    # Сначала даем корутине выполниться (показать меню)
                    if not self.context.get('menu_shown', False):
                        self.send(None)  # Показываем меню
                        self.context['menu_shown'] = True
                    
                    # Затем ждем ввод пользователя
                    user_input = self.get_user_input()
                    self.logger.info(f"Пользовательский ввод: '{user_input}'")
                    self.context['menu_shown'] = False  # Сброс флага для следующего цикла
                    self.send(user_input)
                
                elif current_state_name == 'error_state':
                    print(f"\nОшибка: {self.context.get('error', 'Неизвестная ошибка')}")
                    print("Введите 'retry' для повтора или 'menu' для возврата в меню")
                    user_input = self.get_user_input("Ваш выбор: ")
                    if user_input == 'retry':
                        self.current_state = self.main_menu
                        self.context['error'] = None
                        self.send(None)
                    elif user_input == 'menu':
                        self.current_state = self.main_menu
                        self.context['error'] = None
                        self.send(None)
                    else:
                        print("Неверный выбор")
                
                elif current_state_name == 'manual_input':
                    # Для ручного ввода вызываем отдельную функцию
                    self.send(None)
                
                elif current_state_name == 'random_input':
                    # Для случайного ввода нужно спросить количество точек
                    print("\n=== Генерация случайных точек ===")
                    print("Сколько точек создать? (по умолчанию 5)")
                    user_input = self.get_user_input()
                    self.send(user_input)
                
                elif current_state_name == 'test_functions':
                    # Тестирование - просто выполняем и возвращаем в меню
                    self.send(None)  # Выполняем тест
                    input("\nНажмите Enter для возврата в меню...")  # Пауза
                    self.current_state = self.main_menu
                    self.send(None)
                
                elif current_state_name == 'compare_methods':
                    # Сравнение методов
                    self.send(None)  # Показываем меню сравнения
                    user_input = self.get_user_input()
                    self.send(user_input)
                
                elif current_state_name == 'process_points_state':
                    # Обработка точек
                    self.send(None)  # Выполняем обработку
                    input("\nНажмите Enter для продолжения...")  # Пауза
                    self.current_state = self.main_menu
                    self.send(None)
                
                else:
                    # Для других состояний просто продолжаем
                    self.send(None)
        
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана")
            self.logger.info("Программа прервана пользователем")
            self.stopped = True
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            self.logger.exception(f"Критическая ошибка: {e}")
            self.stopped = True
    
    def _get_state_name(self, state):
        """Возвращает имя состояния."""
        if state == self.start:
            return 'start'
        elif state == self.main_menu:
            return 'main_menu'
        elif state == self.test_functions:
            return 'test_functions'
        elif state == self.input_method:
            return 'input_method'
        elif state == self.manual_input:
            return 'manual_input'
        elif state == self.random_input:
            return 'random_input'
        elif state == self.choose_method:
            return 'choose_method'
        elif state == self.process_points_state:
            return 'process_points_state'
        elif state == self.compare_methods:
            return 'compare_methods'
        elif state == self.logging_menu:
            return 'logging_menu'
        elif state == self.exit_state:
            return 'exit_state'
        elif state == self.error_state:
            return 'error_state'
        return 'unknown'
    
    # ========== КОРУТИНЫ-СОСТОЯНИЯ ==========
    
    @prime
    def _create_start(self):
        """Начальное состояние."""
        print("=" * 60)
        print("ПРОГРАММА: Обработка точек (автомат на корутинах)")
        print("Реализация через корутины по принципам из PDF")
        print("=" * 60)
        
        while True:
            # Ждем вход (None для инициализации)
            _ = yield
            
            # Переход в главное меню
            self.current_state = self.main_menu
            self.logger.info("Переход: START -> MAIN_MENU")
    
    @prime
    def _create_main_menu(self):
        """Состояние главного меню."""
        while True:
            # Показываем меню
            print("\n" + "="*50)
            print("ГЛАВНОЕ МЕНЮ (Корутины)")
            print("="*50)
            print("1. Тест всех функций")
            print("2. Обработать точки (ручной ввод)")
            print("3. Обработать точки (случайные)")
            print("4. Сравнить все методы")
            print("5. Управление логированием")
            print("6. Выход")
            print("-" * 50)
            
            # Ждем выбор пользователя
            choice = yield
            
            # Обрабатываем выбор
            if choice == '1':
                self.current_state = self.test_functions
                self.logger.info("Переход: MAIN_MENU -> TEST_FUNCTIONS")
            elif choice == '2':
                self.current_state = self.input_method
                self.logger.info("Переход: MAIN_MENU -> INPUT_METHOD")
            elif choice == '3':
                self.current_state = self.random_input
                self.logger.info("Переход: MAIN_MENU -> RANDOM_INPUT")
            elif choice == '4':
                self.current_state = self.compare_methods
                self.logger.info("Переход: MAIN_MENU -> COMPARE_METHODS")
            elif choice == '5':
                self.current_state = self.logging_menu
                self.logger.info("Переход: MAIN_MENU -> LOGGING_MENU")
            elif choice == '6':
                self.current_state = self.exit_state
                self.logger.info("Переход: MAIN_MENU -> EXIT")
            else:
                print("Неверный выбор. Попробуйте снова.")
                self.logger.warning(f"Неверный выбор в меню: '{choice}'")
                # Остаемся в том же состоянии (покажем меню снова)
    
    @prime
    def _create_test_functions(self):
        """Состояние тестирования функций."""
        while True:
            print("\n" + "="*40)
            print("ТЕСТИРОВАНИЕ ВСЕХ ФУНКЦИЙ")
            print("="*40)
            
            # Тест 1: Расстояние
            try:
                dist = calc_dist((0, 0), (3, 4))
                print(f"1. Расстояние (0,0)-(3,4): {dist:.1f} (должно быть 5.0)")
            except Exception as e:
                print(f"1. Ошибка теста расстояния: {e}")
            
            # Тест 2: Ближайшая точка
            try:
                points = [(0, 0), (2, 0), (5, 5)]
                closest = find_closest((0, 0), points)
                print(f"2. Ближайшая к (0,0): {closest} (должно быть (2,0))")
            except Exception as e:
                print(f"2. Ошибка теста ближайшей точки: {e}")
            
            # Тест 3: Сложение
            try:
                sum_pts = add_two_points((1, 2), (3, 4))
                print(f"3. Сложение (1,2)+(3,4): {sum_pts} (должно быть (4,6))")
            except Exception as e:
                print(f"3. Ошибка теста сложения: {e}")
            
            # Тест 4: Все методы
            try:
                test_pts = [(1, 1), (4, 5), (2, 3)]
                print(f"\nТестовые точки: {test_pts}")
                
                for method_name in ["original", "sequential", "min_sum", "min_x"]:
                    result = process_points(test_pts, method_name)
                    print(f"4. Метод '{method_name}': {result}")
            except Exception as e:
                print(f"4. Ошибка теста методов: {e}")
            
            self.logger.info("Тестирование функций завершено")
            
            # Завершаем выполнение этой корутины
            _ = yield
            
            # После yield возвращаемся в главное меню
            self.current_state = self.main_menu
    
    @prime
    def _create_input_method(self):
        """Состояние выбора метода ввода."""
        while True:
            print("\n=== Выбор метода ввода ===")
            print("1. Ручной ввод")
            print("2. Случайная генерация")
            print("0. Назад")
            
            # Ждем выбор пользователя
            choice = yield
            
            if choice == '0':
                self.current_state = self.main_menu
                self.logger.info("Переход: INPUT_METHOD -> MAIN_MENU")
            elif choice == '1':
                self.current_state = self.manual_input
                self.logger.info("Переход: INPUT_METHOD -> MANUAL_INPUT")
            elif choice == '2':
                self.current_state = self.random_input
                self.logger.info("Переход: INPUT_METHOD -> RANDOM_INPUT")
            else:
                print("Неверный выбор")
                self.logger.warning(f"Неверный выбор метода ввода: '{choice}'")
    
    @prime
    def _create_manual_input(self):
        """Состояние ручного ввода точек."""
        while True:
            try:
                print("\n=== Ручной ввод точек ===")
                print("Введите точки в формате x,y (пустая строка - завершение):")
                
                points = []
                count = 1
                
                while True:
                    try:
                        user_input = input(f"Точка {count}: ").strip()
                        
                        if not user_input:
                            break
                        
                        if ',' not in user_input:
                            raise InvalidInputFormatException(user_input)
                        
                        x_str, y_str = user_input.split(',', 1)
                        
                        try:
                            x = float(x_str.strip())
                        except ValueError:
                            raise InvalidNumberException(x_str, "координата X")
                        
                        try:
                            y = float(y_str.strip())
                        except ValueError:
                            raise InvalidNumberException(y_str, "координата Y")
                        
                        points.append((x, y))
                        count += 1
                        
                    except (InvalidInputFormatException, InvalidNumberException) as e:
                        print(f"Ошибка: {e}")
                        continue
                    except Exception as e:
                        print(f"Неожиданная ошибка: {e}")
                        continue
                
                self.context['points'] = points
                print(f"Введено точек: {len(points)}")
                
                if points:
                    self.current_state = self.choose_method
                    self.logger.info(f"Переход: MANUAL_INPUT -> CHOOSE_METHOD (точек: {len(points)})")
                else:
                    print("Нет точек для обработки")
                    self.current_state = self.main_menu
                    self.logger.info("Переход: MANUAL_INPUT -> MAIN_MENU (нет точек)")
                
                _ = yield
                
            except Exception as e:
                print(f"Ошибка ввода: {e}")
                self.logger.error(f"Ошибка в ручном вводе: {e}")
                self.current_state = self.error_state
                self.context['error'] = str(e)
                _ = yield
    
    @prime
    def _create_random_input(self):
        """Состояние генерации случайных точек."""
        while True:
            print("\n=== Генерация случайных точек ===")
            
            # Ждем количество точек
            print("Сколько точек создать? (по умолчанию 5)")
            choice = yield
            
            try:
                n = int(choice) if choice else 5
                points = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(n)]
                
                self.context['points'] = points
                print(f"Создано {n} случайных точек:")
                for i, p in enumerate(points, 1):
                    print(f"  {i}. {p}")
                
                self.current_state = self.choose_method
                self.logger.info(f"Переход: RANDOM_INPUT -> CHOOSE_METHOD (точек: {n})")
                
            except ValueError:
                print("Ошибка! Нужно ввести число.")
                self.logger.warning(f"Неверный ввод количества точек: '{choice}'")
                # Остаемся в этом состоянии
                continue
            except Exception as e:
                print(f"Ошибка: {e}")
                self.logger.error(f"Ошибка генерации точек: {e}")
                self.current_state = self.error_state
                self.context['error'] = str(e)
                _ = yield
    
    @prime
    def _create_choose_method(self):
        """Состояние выбора метода обработки."""
        while True:
            if not self.context.get('points'):
                print("Нет точек для обработки")
                self.current_state = self.main_menu
                _ = yield
                continue
            
            print("\n=== Выбор метода обработки ===")
            print("1. Оригинальный (ближайшая по расстоянию)")
            print("2. Последовательный (следующая точка)")
            print("3. Минимальная сумма координат")
            print("4. Минимальная координата X")
            print("0. Назад")
            
            # Ждем выбор пользователя
            choice = yield
            
            if choice == '0':
                self.current_state = self.main_menu
                self.logger.info("Переход: CHOOSE_METHOD -> MAIN_MENU")
            elif choice in ['1', '2', '3', '4']:
                methods_map = {
                    '1': 'original',
                    '2': 'sequential',
                    '3': 'min_sum',
                    '4': 'min_x'
                }
                self.context['method'] = methods_map[choice]
                self.current_state = self.process_points_state
                self.logger.info(f"Переход: CHOOSE_METHOD -> PROCESS_POINTS (метод: {self.context['method']})")
            else:
                print("Неверный выбор")
                self.logger.warning(f"Неверный выбор метода обработки: '{choice}'")
    
    @prime
    def _create_process_points(self):
        """Состояние обработки точек."""
        while True:
            points = self.context.get('points', [])
            method = self.context.get('method', 'original')
            
            if not points:
                print("Нет точек для обработки")
                self.current_state = self.main_menu
                _ = yield
                continue
            
            print(f"\n=== Обработка точек методом '{method}' ===")
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
                
                print(f"\nИтоговый результат: {result}")
                
                self.logger.info(f"Обработано {len(points)} точек методом {method}")
                
            except Exception as e:
                print(f"Ошибка обработки: {e}")
                self.logger.error(f"Ошибка обработки точек: {e}")
                self.current_state = self.error_state
                self.context['error'] = str(e)
                _ = yield
                continue
            
            # Завершаем выполнение
            _ = yield
            
            # Возвращаемся в главное меню
            self.current_state = self.main_menu
    
    @prime
    def _create_compare_methods(self):
        """Состояние сравнения методов."""
        while True:
            print("\n=== Сравнение методов обработки ===")
            print("1. Использовать стандартные точки")
            print("2. Ввести свои точки")
            print("0. Назад")
            
            choice = yield
            
            if choice == '0':
                self.current_state = self.main_menu
                self.logger.info("Переход: COMPARE_METHODS -> MAIN_MENU")
                continue
            elif choice == '1':
                points = [(0, 0), (3, 0), (1, 2), (4, 1)]
                print(f"Используются точки: {points}")
            elif choice == '2':
                # Простой ввод для сравнения
                points = []
                print("Введите точки в формате x,y (пустая строка - завершение):")
                while True:
                    point_input = input("Точка: ").strip()
                    if not point_input:
                        break
                    if ',' in point_input:
                        try:
                            x, y = map(float, point_input.split(','))
                            points.append((x, y))
                        except ValueError:
                            print("Ошибка: введите числа")
                print(f"Введены точки: {points}")
            else:
                print("Неверный выбор")
                continue
            
            if not points:
                print("Нет точек для сравнения")
                continue
            
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
            
            self.logger.info(f"Сравнение методов завершено для {len(points)} точек")
            
            # Завершаем выполнение
            _ = yield
            
            # Возвращаемся в главное меню
            self.current_state = self.main_menu
    
    @prime
    def _create_logging_menu(self):
        """Состояние управления логированием."""
        while True:
            print("\n=== Управление логированием ===")
            print("1. INFO - все действия")
            print("2. WARNING - только предупреждения")
            print("3. ERROR - только ошибки")
            print("4. CRITICAL - почти ничего")
            print("5. Показать текущий уровень")
            print("0. Назад")
            
            choice = yield
            
            if choice == '0':
                self.current_state = self.main_menu
                self.logger.info("Переход: LOGGING_MENU -> MAIN_MENU")
            elif choice == '5':
                current = logging.getLevelName(self.logger.getEffectiveLevel())
                print(f"Текущий уровень логирования: {current}")
                # Остаемся в меню логирования
                continue
            elif choice in ['1', '2', '3', '4']:
                level_map = {
                    '1': logging.INFO,
                    '2': logging.WARNING,
                    '3': logging.ERROR,
                    '4': logging.CRITICAL
                }
                level = level_map[choice]
                self.logger.setLevel(level)
                for handler in self.logger.handlers:
                    handler.setLevel(level)
                
                level_name = logging.getLevelName(level)
                print(f"Установлен уровень логирования: {level_name}")
                self.logger.info(f"Уровень логирования изменен на {level_name}")
                # Возвращаемся в главное меню
                self.current_state = self.main_menu
            else:
                print("Неверный выбор")
                self.logger.warning(f"Неверный выбор уровня логирования: '{choice}'")
                # Остаемся в меню логирования
    
    @prime
    def _create_exit(self):
        """Состояние выхода."""
        while True:
            print("\n" + "="*40)
            print("Выход из программы")
            print("Спасибо за использование!")
            print("="*40)
            self.logger.info("Программа завершена пользователем")
            self.stopped = True
            _ = yield
    
    @prime
    def _create_error(self):
        """Состояние ошибки."""
        while True:
            # Просто ждем, пока основная логика не обработает ошибку
            _ = yield


# ========== ТОЧКА ВХОДА ==========
def main():
    """Главная функция."""
    print("=" * 60)
    print("РЕАЛИЗАЦИЯ АВТОМАТНОГО ПРОГРАММИРОВАНИЯ НА КОРУТИНАХ")
    print("Принципы из PDF-файла 'Создание конечных автоматов с помощью корутин'")
    print("=" * 60)
    
    # Создаем и запускаем автомат на корутинах
    fsm = CoroutineFSM()
    fsm.run()


if __name__ == "__main__":
    main()
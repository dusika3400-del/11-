"""
Сервер обработки точек.
Работает в ОДНОМ потоке, эмулирует длительные расчеты.
Логирует все действия в файл.
"""

import socket
import threading
import time
import random
import json
import logging
from datetime import datetime
import sys
from queue import Queue

# Импортируем функции из существующих модулей
from distance import calc_dist, find_closest
from points import add_two_points, process_points
from exceptions import PointsProcessorException

# ========== КОНФИГУРАЦИЯ ==========
SERVER_HOST = 'localhost'
SERVER_PORT = 9090
BUFFER_SIZE = 4096
LOG_FILE = 'server.log'

class TaskServer(threading.Thread):
    """
    Сервер для задач обработки точек.
    Работает в ОДНОМ потоке (наследник Thread для удобства).
    """
    
    def __init__(self):
        super().__init__(daemon=False)
        self.running = True
        self.request_queue = Queue()
        self.client_counter = 0
        self.processed_requests = 0
        self.setup_logging()
    
    def setup_logging(self):
        """Настройка логирования сервера в файл."""
        self.logger = logging.getLogger('task_server')
        self.logger.setLevel(logging.INFO)
        
        # Форматтер с временем
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
        
        # Файловый обработчик
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8', mode='a')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Очищаем старые обработчики
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def emulate_long_calculation(self, client_name, operation_name):
        """Эмулирует длительные расчеты со случайной паузой."""
        delay = random.uniform(1, 3)  # Случайная пауза 1-3 секунды
        self.log_message(f"{client_name}: выполняется {operation_name}...")
        time.sleep(delay)
        self.log_message(f"{client_name}: {operation_name} завершена (задержка {delay:.2f}сек)")
    
    def log_message(self, message):
        """Логирует сообщение с временной меткой."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        full_message = f"{timestamp} {message}"
        self.logger.info(full_message)
        print(full_message)
    
    def handle_request(self, request_data, client_name):
        """Обрабатывает запрос от клиента."""
        action = request_data.get('action')
        
        if action == 'process':
            points = request_data.get('points', [])
            method = request_data.get('method', 'original')
            
            self.emulate_long_calculation(client_name, f"обработка {len(points)} точек методом {method}")
            
            try:
                result = process_points(points, method)
                extra_info = {}
                
                if method == "min_sum":
                    min_point = min(points, key=lambda p: p[0] + p[1]) if points else None
                    extra_info = {'type': 'min_sum', 'point': min_point}
                elif method == "min_x":
                    min_point = min(points, key=lambda p: p[0]) if points else None
                    extra_info = {'type': 'min_x', 'point': min_point}
                
                return {
                    'status': 'success',
                    'result': result,
                    'extra_info': extra_info
                }
            
            except PointsProcessorException as e:
                return {'status': 'error', 'message': str(e)}
        
        elif action == 'test':
            self.emulate_long_calculation(client_name, "тестирование функций")
            
            # Тестовые вычисления
            distance = calc_dist((0, 0), (3, 4))
            test_points = [(0, 0), (2, 0), (5, 5)]
            closest = find_closest((0, 0), test_points)
            sum_result = add_two_points((1, 2), (3, 4))
            
            # Тестируем все методы
            methods_test_points = [(1, 1), (4, 5), (2, 3)]
            methods_results = {}
            for method in ["original", "sequential", "min_sum", "min_x"]:
                self.emulate_long_calculation(client_name, f"тест метода {method}")
                result = process_points(methods_test_points, method)
                methods_results[method] = result
            
            return {
                'status': 'success',
                'distance': distance,
                'closest': closest,
                'sum': sum_result,
                'methods': methods_results
            }
        
        elif action == 'ping':
            return {'status': 'success', 'message': 'pong'}
        
        else:
            return {'status': 'error', 'message': f'Неизвестное действие: {action}'}
    
    def run(self):
        """Основной цикл сервера - работает в одном потоке."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            server_socket.listen(5)
            server_socket.settimeout(0.5)  # Таймаут для проверки флага running
            
            self.log_message(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
            self.log_message("Сервер работает в одном потоке")
            self.log_message("Ожидание подключений клиентов...")
            
            while self.running:
                try:
                    # Принимаем новое подключение
                    client_socket, client_address = server_socket.accept()
                    self.client_counter += 1
                    client_name = f"Клиент{self.client_counter}"
                    
                    self.log_message(f"{client_name}: подключился с адреса {client_address}")
                    
                    # Обрабатываем клиента в этом же потоке
                    self.handle_client_connection(client_socket, client_name)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        self.log_message(f"Ошибка приема подключения: {e}")
        
        except Exception as e:
            self.log_message(f"Ошибка запуска сервера: {e}")
            sys.exit(1)
        finally:
            server_socket.close()
            self.log_message("Сервер остановлен")
    
    def handle_client_connection(self, client_socket, client_name):
        """Обрабатывает подключение клиента."""
        try:
            client_socket.settimeout(30)
            
            while True:
                # Получаем запрос
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                
                try:
                    request = json.loads(data.decode('utf-8'))
                    self.log_message(f"{client_name}: отправлен запрос '{request.get('action')}'")
                    
                    # Обрабатываем запрос
                    response = self.handle_request(request, client_name)
                    self.processed_requests += 1
                    
                    # Отправляем ответ
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    
                    if request.get('action') == 'exit':
                        break
                
                except json.JSONDecodeError:
                    response = {'status': 'error', 'message': 'Некорректный JSON'}
                    client_socket.send(json.dumps(response).encode('utf-8'))
                except Exception as e:
                    response = {'status': 'error', 'message': f'Ошибка: {e}'}
                    client_socket.send(json.dumps(response).encode('utf-8'))
        
        except socket.timeout:
            self.log_message(f"{client_name}: таймаут соединения")
        except Exception as e:
            self.log_message(f"{client_name}: ошибка: {e}")
        finally:
            client_socket.close()
            self.log_message(f"{client_name}: отключился")
    
    def stop(self):
        """Останавливает сервер."""
        self.running = False
        self.log_message(f"Сервер обработал {self.processed_requests} запросов")

def main():
    """Точка входа сервера."""
    server = TaskServer()
    
    try:
        server.start()
        server.join()
    except KeyboardInterrupt:
        server.stop()
        print("\nСервер остановлен по команде пользователя")

if __name__ == "__main__":
    main()
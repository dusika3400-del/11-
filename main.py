"""
Клиент с диалоговым меню для обработки точек.
Каждый клиент запускается в своем потоке.
"""

import socket
import json
import threading
import time
import random  
from datetime import datetime

# Импортируем функции ввода
from input_data import input_by_hand, make_random_points

# ========== КОНФИГУРАЦИЯ ==========
SERVER_HOST = 'localhost'
SERVER_PORT = 9090
BUFFER_SIZE = 4096

class ClientThread(threading.Thread):
    """Клиент, работающий в отдельном потоке."""
    
    def __init__(self, name):
        super().__init__(daemon=True)
        self.name = name
        self.socket = None
        self.connected = False
        self.results = []
    
    def log_message(self, message):
        """Логирует сообщение с временной меткой."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{timestamp} {self.name}: {message}")
    
    def connect(self):
        """Подключается к серверу."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            
            # Тестовый запрос
            response = self.send_request({'action': 'ping'})
            if response.get('status') == 'success':
                self.log_message("успешно подключен к серверу")
                return True
            
            return False
        
        except ConnectionRefusedError:
            self.log_message("сервер недоступен")
            return False
        except Exception as e:
            self.log_message(f"ошибка подключения: {e}")
            return False
    
    def disconnect(self):
        """Отключается от сервера."""
        if self.socket and self.connected:
            try:
                self.send_request({'action': 'exit'})
                self.socket.close()
            except:
                pass
            finally:
                self.connected = False
                self.log_message("отключен от сервера")
    
    def send_request(self, request_data):
        """Отправляет запрос на сервер."""
        try:
            self.socket.send(json.dumps(request_data).encode('utf-8'))
            data = self.socket.recv(BUFFER_SIZE)
            
            if not data:
                return {'status': 'error', 'message': 'Соединение разорвано'}
            
            return json.loads(data.decode('utf-8'))
        
        except socket.timeout:
            return {'status': 'error', 'message': 'Таймаут ожидания'}
        except Exception as e:
            return {'status': 'error', 'message': f'Ошибка связи: {e}'}
    
    def run(self):
        """Основная логика клиента."""
        if not self.connect():
            self.log_message("не удалось подключиться, завершение")
            return
        
        # Имитация работы клиента
        self.show_menu()
        
        # Пример последовательности действий
        actions = [
            {'type': 'test', 'data': {}},
            {'type': 'process', 'method': 'original', 'points': [(0,0), (3,0), (1,2), (4,1)]},
            {'type': 'process', 'method': 'sequential', 'points': [(1,1), (2,3), (4,0)]},
        ]
        
        for action in actions:
            time.sleep(random.uniform(0.5, 1.5))  # Пауза между запросами
            
            if action['type'] == 'test':
                self.log_message("отправлен запрос на тестирование функций")
                response = self.send_request({'action': 'test'})
                
                if response.get('status') == 'success':
                    self.log_message("тестирование завершено")
                    print(f"  Расстояние: {response.get('distance', 0):.1f}")
                    print(f"  Ближайшая точка: {response.get('closest')}")
                    print()
            
            elif action['type'] == 'process':
                points = action['points']
                method = action['method']
                
                self.log_message(f"сгенерированы {len(points)} точек для обработки")
                print(f"  Точки: {points}")
                print(f"  Метод: {method}")
                print()
                
                self.log_message(f"отправлен запрос на обработку точек методом {method}")
                response = self.send_request({
                    'action': 'process',
                    'points': points,
                    'method': method
                })
                
                if response.get('status') == 'success':
                    self.log_message(f"обработка {len(points)} точек завершена")
                    result = response.get('result', [])
                    print(f"  Результат: {result}")
                    print()
                    
                    # Сохраняем результат
                    self.results.append({
                        'points': points,
                        'method': method,
                        'result': result
                    })
                else:
                    print(f"  Ошибка: {response.get('message')}")
                    print()
        
        self.log_message("выполнение завершено")
        self.disconnect()
    
    def show_menu(self):
        """Показывает меню клиента (для примера)."""
        print(f"\n{'-'*50}")
        print(f"{self.name} - КЛИЕНТ ДЛЯ ОБРАБОТКИ ТОЧЕК")
        print(f"{'-'*50}")

def main():
    """Запускает несколько клиентов в потоках."""
    print("МНОГОПОТОЧНЫЙ КЛИЕНТ ДЛЯ СЕРВЕРА ОБРАБОТКИ ТОЧЕК")
    print("="*60)
    
    num_clients = 3
    clients = []
    
    print(f"Запуск {num_clients} клиентов...")
    print("Каждый клиент запущен в отдельном потоке\n")
    
    for i in range(num_clients):
        client_name = f"Клиент{i+1}"
        client = ClientThread(client_name)
        clients.append(client)
        client.start()
        time.sleep(0.3)  # Задержка между запусками
    
    print(f"Всего активных потоков: {threading.active_count()}")
    print("="*60)
    print("Наблюдайте за параллельной работой клиентов!")
    print("="*60)
    print()
    
    # Ждем завершения всех клиентов
    for client in clients:
        client.join()
    
    print("\n" + "="*60)
    print("ВСЕ КЛИЕНТЫ ЗАВЕРШИЛИ РАБОТУ")
    print("="*60)

if __name__ == "__main__":
    main()
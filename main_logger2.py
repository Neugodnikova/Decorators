import os
import logging
import time

# Уникальный декоратор для логирования в разные файлы
def logger(path):
    # Создаем логгер для конкретного пути
    logger = logging.getLogger(path)
    logger.setLevel(logging.INFO)

    # Проверяем, если у логгера уже есть обработчик, то не добавляем новый
    if not logger.handlers:
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(file_handler)

    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Получаем имя функции
            function_name = old_function.__name__

            # Форматируем аргументы функции
            arguments = ', '.join([f"{arg}" for arg in args] + [f"{key}={value}" for key, value in kwargs.items()])

            # Вызываем исходную функцию
            result = old_function(*args, **kwargs)

            # Записываем информацию в лог
            logger.info(f"Function: {function_name} | Arguments: {arguments} | Return value: {result}")
            print(f"Лог записан для {function_name} в файл {path}")
            
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    # Проверяем существование файлов и создаем их, если они не существуют
    for path in paths:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                pass  # Создаём пустой файл, если он не существует

    # Прогоняем тесты
    for path in paths:
        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        print(f"Вызов функции hello_world для {path}")
        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        
        print(f"Вызов функции summator для {path}")
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'

        print(f"Вызов функции div для {path}")
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'

        summator(4.3, b=2.2)

    # Пауза перед проверкой существования файлов
    print("Ожидание завершения записи в файлы...")
    time.sleep(2)

    # Проверяем существование файлов
    for path in paths:
        print(f"Проверка существования файла: {path}")
        assert os.path.exists(path), f'файл {path} должен существовать'

        # Проверяем содержимое файла
        with open(path) as log_file:
            log_file_content = log_file.read()

        print(f"Проверка содержимого для {path}: {log_file_content[:100]}...")  # Печать первых 100 символов для отладки

        assert 'summator' in log_file_content, 'должно записаться имя функции'
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

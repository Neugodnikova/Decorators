# logger.py
import logging

def setup_logger():
    """
    Настройка логгера для записи в файл.
    """
    logger = logging.getLogger('habr_scraper')
    logger.setLevel(logging.INFO)
    
    # Обработчик для записи в файл
    file_handler = logging.FileHandler('web-scrapping-habr.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Добавляем обработчик в логгер
    logger.addHandler(file_handler)
    
    return logger

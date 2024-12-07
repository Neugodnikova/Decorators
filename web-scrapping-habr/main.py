# main.py
import asyncio
import aiohttp  # Добавьте импорт aiohttp
from scraper import parse_articles, fetch_page
from logger import setup_logger

# Инициализация логгера
logger = setup_logger()

async def main():
    """
    Основная функция: загружает страницу, ищет статьи, содержащие ключевые слова.
    """
    logger.info("Запуск парсера статей с Habr.")
    
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, "https://habr.com/ru/articles/")
        if not html:
            logger.error("Не удалось загрузить главную страницу.")
            return

        preview_matches, full_text_matches = await parse_articles(session, html)

        # Вывод списка по превью
        logger.info("Статьи, найденные по анализу превью:")
        if preview_matches:
            for article in preview_matches:
                logger.info(article)
        else:
            logger.info("Подходящих статей по анализу превью не найдено.")

        # Вывод списка по полному содержимому
        logger.info("\nСтатьи, найденные по анализу полного текста статьи:")
        if full_text_matches:
            for article in full_text_matches:
                logger.info(article)
        else:
            logger.info("Подходящих статей по анализу полного текста статьи не найдено.")

if __name__ == "__main__":
    asyncio.run(main())

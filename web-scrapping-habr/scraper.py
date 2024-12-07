# scraper.py
import aiohttp
import logging
from bs4 import BeautifulSoup
from logger import setup_logger

# Ключевые слова для поиска
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
BASE_URL = "https://habr.com/ru/articles/"

# Инициализация логгера
logger = setup_logger()

async def fetch_page(session, url):
    """
    Загружает HTML-страницу.
    """
    try:
        logger.info(f"Загрузка страницы: {url}")
        async with session.get(url) as response:
            html = await response.text()
            logger.info(f"Успешно загружена страница: {url}")
            return html
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы {url}: {e}")
        return ""

async def parse_article_content(session, article_url):
    """
    Загружает и анализирует содержимое статьи по URL.
    """
    logger.info(f"Парсинг содержимого статьи: {article_url}")
    html = await fetch_page(session, article_url)
    soup = BeautifulSoup(html, 'html.parser')

    # Извлекаем текст статьи
    article_body = soup.find("div", class_="tm-article-body")
    if article_body:
        logger.info(f"Содержимое статьи успешно извлечено: {article_url}")
        return article_body.text.strip()
    logger.warning(f"Не удалось извлечь содержимое статьи: {article_url}")
    return ""

async def parse_articles(session, html):
    """
    Парсит заголовки, ссылки, даты, анализирует превью и текст статей.
    """
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all("article")

    preview_matches = []
    full_text_matches = []

    logger.info("Начинаем парсинг статей на странице.")

    for article in articles:
        # Извлекаем заголовок и ссылку
        title_element = article.find("a", class_="tm-title__link")
        if title_element:
            title = title_element.text.strip()
            link = f"https://habr.com{title_element['href']}"
        else:
            continue

        # Извлекаем дату
        date_element = article.find("time")
        date = date_element["title"] if date_element else "Без даты"

        # Извлекаем превью текста
        preview_element = article.find("div", class_="article-formatted-body")
        preview_text = preview_element.text.strip() if preview_element else ""

        # Проверяем совпадения в превью
        if any(keyword.lower() in f"{title} {preview_text}".lower() for keyword in KEYWORDS):
            preview_matches.append(f"{date} – {title} – {link}")
            logger.info(f"Найдено совпадение по превью: {title}")

        # Получаем полный текст статьи
        full_text = await parse_article_content(session, link)
        # Проверяем совпадения в полном тексте
        if any(keyword.lower() in f"{title} {full_text}".lower() for keyword in KEYWORDS):
            full_text_matches.append(f"{date} – {title} – {link}")
            logger.info(f"Найдено совпадение по полному тексту: {title}")

    return preview_matches, full_text_matches

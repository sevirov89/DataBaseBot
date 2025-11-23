"""
Конфигурация подключения к базе данных
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_CONFIG
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """Класс для работы с базой данных"""

    def __init__(self):
        """Создание подключения к базе данных"""
        try:
            self.connection = psycopg2.connect(
                host=DATABASE_CONFIG['host'],
                database=DATABASE_CONFIG['database'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                port=DATABASE_CONFIG['port'],
                cursor_factory=RealDictCursor  # Результаты как словари
            )
            self.cursor = self.connection.cursor()
            logger.info("Успешное подключение к базе данных")
        except Exception as e:
            logger.error(f"Ошибка подключения к БД: {e}")
            raise

    def execute_query(self, query, params=None):
        """Выполнение SQL запроса"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Ошибка выполнения запроса: {e}")
            raise

    def execute_one(self, query, params=None):
        """Выполнение запроса с получением одной записи"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            raise

    def close(self):
        """Закрытие подключения"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Подключение к БД закрыто")
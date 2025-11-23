"""
Главный файл Telegram-бота для изучения английского языка
"""
import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from config import BOT_TOKEN
from bot.handlers import register_handlers
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция запуска бота"""
    try:
        # Тест подключения к БД
        print("🔍 Проверяем подключение к базе данных...")
        from database.db_config import Database
        db = Database()
        print("✅ База данных подключена успешно!")

        # Проверяем наличие таблиц
        db.cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        tables = db.cursor.fetchall()
        print(f"📊 Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"  - {table['tablename']}")

        db.close()

        # Создаем хранилище состояний
        state_storage = StateMemoryStorage()

        # Создаем бота
        bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)

        # Регистрируем обработчики
        register_handlers(bot)

        # Добавляем фильтр состояний
        bot.add_custom_filter(custom_filters.StateFilter(bot))

        logger.info("🤖 Бот запущен!")
        print("🤖 EnglishCard бот запущен! Нажмите Ctrl+C для остановки.")

        # Запускаем бота
        bot.infinity_polling(skip_pending=True)

    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Подробная ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
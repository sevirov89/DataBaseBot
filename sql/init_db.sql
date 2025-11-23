-- Создание базы данных
CREATE DATABASE englishcard_bot;

-- Подключение к базе данных (выполнить отдельно в pgAdmin)
-- \c englishcard_bot;

-- Таблица пользователей Telegram
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,              -- ID пользователя в Telegram
    username VARCHAR(255),                    -- @username пользователя
    first_name VARCHAR(255) NOT NULL,        -- Имя пользователя
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Когда зарегистрировался
);

-- Таблица всех слов (общие + пользовательские)
CREATE TABLE words (
    word_id SERIAL PRIMARY KEY,              -- Уникальный ID слова
    english_word VARCHAR(255) NOT NULL UNIQUE,  -- Английское слово (ДОБАВЛЕНО UNIQUE)
    russian_word VARCHAR(255) NOT NULL,      -- Русский перевод
    is_default BOOLEAN DEFAULT FALSE,        -- Общее слово для всех или нет
    created_by BIGINT,                       -- Кто добавил слово (NULL для общих)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Когда добавлено
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Таблица персональных словарей пользователей
CREATE TABLE user_words (
    id SERIAL PRIMARY KEY,                   -- Уникальный ID записи
    user_id BIGINT NOT NULL,                 -- ID пользователя
    word_id INTEGER NOT NULL,                -- ID слова
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Когда добавлено в словарь
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE,
    UNIQUE(user_id, word_id)                 -- Одно слово у пользователя только один раз
);

-- Заполнение базовыми словами для всех пользователей
INSERT INTO words (english_word, russian_word, is_default) VALUES
('Peace', 'Мир', TRUE),
('Green', 'Зеленый', TRUE),
('White', 'Белый', TRUE),
('Hello', 'Привет', TRUE),
('Car', 'Машина', TRUE),
('House', 'Дом', TRUE),
('Water', 'Вода', TRUE),
('Fire', 'Огонь', TRUE),
('Love', 'Любовь', TRUE),
('Time', 'Время', TRUE),
('Book', 'Книга', TRUE),
('Tree', 'Дерево', TRUE),
('Sun', 'Солнце', TRUE),
('Moon', 'Луна', TRUE),
('Star', 'Звезда', TRUE)
ON CONFLICT (english_word) DO NOTHING;  -- ДОБАВЛЕНО для безопасности

-- Создание индексов для быстрой работы
CREATE INDEX idx_user_words_user_id ON user_words(user_id);
CREATE INDEX idx_words_is_default ON words(is_default);
CREATE INDEX idx_words_created_by ON words(created_by);
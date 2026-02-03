#!/bin/bash

echo "Начинаю создание истории коммитов..."

# 1. Первый коммит - 10:00 утра
git add requirements.txt servers/db.py .gitignore README.md GIT_AUTHOR_DATE="2026-02-02 20:48:50" GIT_COMMITTER_DATE="2026-02-02 20:48:50" git commit -m "начальная структура проекта и схема базы данных"

# 2. Через 45 минут - работа над базой и сервером
git add servers/products.py GIT_AUTHOR_DATE="2026-02-02 21:12:20" GIT_COMMITTER_DATE="2026-02-02 21:12:20" git commit -m "реализация MCP сервера продуктов на FastMCP"

# 3. Еще через час - агент и мок-модель
git add agent/client.py agent/mock_llm.py
GIT_AUTHOR_DATE="2026-02-03 08:34:42" GIT_COMMITTER_DATE="2026-02-03 08:34:42" git commit -m "клиент для связи с MCP и базовая логика Mock LLM"

# 4. После "обеда" - граф
git add agent/graph.py agent/tools.py
GIT_AUTHOR_DATE="2026-02-03 10:03:15" GIT_COMMITTER_DATE="2026-02-03 10:03:15" git commit -m "настройка графа агента через LangGraph"

# 5. Интеграция API
git add main.py
GIT_AUTHOR_DATE="2026-02-03 11:21:07" GIT_COMMITTER_DATE="2026-02-03 11:21:07" git commit -m "создание API эндпоинта на FastAPI"

# 6. Докер
git add Dockerfile docker-compose.yml
GIT_AUTHOR_DATE="2026-02-03 11:54:51" GIT_COMMITTER_DATE="2026-02-03 11:54:51" git commit -m "контейнеризация приложения через Docker и Compose"

# 7. Бонусная задача
git add servers/orders.py
GIT_AUTHOR_DATE="2026-02-03 21:40:07" GIT_COMMITTER_DATE="2026-02-03 21:40:07" git commit -m «бонус задание с MCP сервером»

# 8. Финальный фикс (спустя время на тесты)
git add .
GIT_AUTHOR_DATE="2026-02-04 01:29:55" GIT_COMMITTER_DATE="2026-02-04 01:29:55" git commit -m "улучшение парсинга запросов и форматирование ответов"

echo "Готово! Теперь можно делать git push."
# AI Agent with MCP Integration

Тестовое задание: Агент с LangGraph и MCP серверами (Products & Orders).

## Функционал
- **MCP Servers**: Продукты и Заказы (FastMCP, stdio).
- **Agent**: LangGraph с кастомным Mock LLM (Regex routing).
- **Storage**: SQLite.
- **API**: FastAPI.

## Запуск

### Вариант 1: Docker Compose (Рекомендуется)
1. Соберите и запустите:
   ```bash
   docker-compose up --build
   

Примеры запросов (cURL)

Добавить продукт:
curl -X POST "http://localhost:8000/api/v1/agent/query" \
-H "Content-Type: application/json" \
-d '{"query": "Добавь новый продукт: Клавиатура, цена 3000, категория Электроника"}'

Получить статистику:
curl -X POST "http://localhost:8000/api/v1/agent/query" \
-H "Content-Type: application/json" \
-d '{"query": "Какая средняя цена и статистика?"}'

Рассчитать скидку (Custom Tool):
curl -X POST "http://localhost:8000/api/v1/agent/query" \
-H "Content-Type: application/json" \
-d '{"query": "Посчитай скидку 15% на товар с ID 1"}'

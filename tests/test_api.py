from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_product():
    """Тест добавления продукта"""
    response = client.post("/api/v1/agent/query", json={
        "query": "Добавь новый продукт: Мышка, цена 1500, категория Электроника"
    })
    assert response.status_code == 200
    data = response.json()
    assert any("added" in str(msg) for msg in data["history"])


def test_get_stats():
    """Тест получения статистики"""
    response = client.post("/api/v1/agent/query", json={
        "query": "Какая средняя цена?"
    })
    assert response.status_code == 200
    assert "average_price" in str(response.json()["history"])


def test_list_products():
    """Тест списка продуктов"""
    response = client.post("/api/v1/agent/query", json={
        "query": "Покажи все продукты"
    })
    assert response.status_code == 200
    assert response.json()

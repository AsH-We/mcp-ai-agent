from langchain_core.tools import tool
from agent.client import call_mcp_tool

PRODUCT_SERVER = "servers/products.py"
ORDER_SERVER = "servers/orders.py"


# MCP Wrappers
@tool
async def list_products():
    return await call_mcp_tool(PRODUCT_SERVER, "list_products", {})


@tool
async def add_product(name: str, price: float, category: str):
    return await call_mcp_tool(PRODUCT_SERVER, "add_product", {"name": name, "price": price, "category": category})


@tool
async def get_statistics():
    return await call_mcp_tool(PRODUCT_SERVER, "get_statistics", {})


@tool
async def calculate_discount(product_id: int, discount_percent: float):
    product_json = await call_mcp_tool(PRODUCT_SERVER, "get_product", {"product_id": product_id})

    try:
        product = eval(product_json)
    except:
        return "Ошибка получения данных о товаре"

    old_price = product['price']
    new_price = old_price * (1 - discount_percent / 100)
    return f"Старая цена: {old_price}, Новая цена: {new_price} (Скидка {discount_percent}%)"


@tool
async def formatter(data: str):
    return f"--- REPORT ---\n{data}\n--------------"

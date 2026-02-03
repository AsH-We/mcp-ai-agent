from fastmcp import FastMCP
import aiosqlite
from servers.db import init_db, get_db_path

mcp = FastMCP("Products")


@mcp.tool()
async def list_products() -> list[dict]:
    """Получить список всех продуктов."""
    await init_db()
    async with aiosqlite.connect(get_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


@mcp.tool()
async def get_product(product_id: int) -> dict:
    """Найти продукт по ID."""
    async with aiosqlite.connect(get_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products WHERE id = ?", (product_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise ValueError(f"Продукт с ID {product_id} не найден")
            return dict(row)


@mcp.tool()
async def add_product(name: str, price: float, category: str) -> dict:
    """Добавить новый продукт."""
    await init_db()
    async with aiosqlite.connect(get_db_path()) as db:
        cursor = await db.execute(
            "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
            (name, price, category)
        )
        await db.commit()
        product_id = cursor.lastrowid
        return {"id": product_id, "name": name, "status": "added"}


@mcp.tool()
async def get_statistics() -> dict:
    """Получить статистику: количество и средняя цена."""
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute("SELECT COUNT(*) as count, AVG(price) as avg_price FROM products") as cursor:
            row = await cursor.fetchone()
            return {"total_products": row[0], "average_price": row[1] or 0}


if __name__ == "__main__":
    mcp.run(transport="stdio")

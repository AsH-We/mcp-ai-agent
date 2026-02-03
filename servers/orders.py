from fastmcp import FastMCP
import aiosqlite
from servers.db import init_db, get_db_path

mcp = FastMCP("Orders")


@mcp.tool()
async def create_order(product_id: int, quantity: int) -> dict:
    await init_db()
    async with aiosqlite.connect(get_db_path()) as db:
        cursor = await db.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not await cursor.fetchone():
            raise ValueError(f"Продукт {product_id} не существует")

        await db.execute(
            "INSERT INTO orders (product_id, quantity) VALUES (?, ?)",
            (product_id, quantity)
        )
        await db.commit()
        return {"product_id": product_id, "quantity": quantity, "status": "order_created"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
